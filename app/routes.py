import json
import os
# Used only with fixed, server-defined diagnostic command arrays.
import subprocess  # nosec B404
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from flask import Blueprint, Response, abort, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .db import delete_analysis, get_analysis, get_db, list_analyses, save_analysis
from .metrics import observe
from .services.analyzer import analyze, digest

bp = Blueprint("main", __name__)


def _latest_for_workspace(role, sensor_names, limit=100):
    """Return newest evidence explicitly assigned to a role, then compatible uploads."""
    expected = set(sensor_names)
    for row in list_analyses(limit):
        item = get_analysis(row["id"])
        roles = set(item["result"].get("workspace_roles", []))
        if role in roles:
            return item
        if not roles and expected.intersection(item["result"].get("series", {})):
            return item
    return None


def _run_devsecops_checks(root):
    commands = [
        ("Application tests", [sys.executable, "-m", "pytest", "-q"]),
        ("Python compilation", [sys.executable, "-m", "compileall", "-q", "app"]),
        ("Static security scan", [sys.executable, "-m", "bandit", "-q", "-r", "app"]),
        ("Dependency integrity check", [sys.executable, "-m", "pip", "check"]),
    ]

    def execute(check):
        name, command = check
        started = time.monotonic()
        try:
            # No request value can alter the executable or arguments.
            completed = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=90, check=False)  # nosec B603
            output = (completed.stdout + "\n" + completed.stderr).strip()
            return {"name": name, "passed": completed.returncode == 0, "seconds": round(time.monotonic() - started, 2), "output": output[-4000:] or "Completed without findings."}
        except subprocess.TimeoutExpired:
            return {"name": name, "passed": False, "seconds": 90, "output": "Check exceeded the 90-second safety timeout."}

    with ThreadPoolExecutor(max_workers=len(commands)) as executor:
        return list(executor.map(execute, commands))


@bp.app_context_processor
def globals_for_templates():
    return {
        "product_name": "AquaVigil",
        "prometheus_url": os.getenv("PROMETHEUS_PUBLIC_URL", "http://localhost:9090"),
        "grafana_url": os.getenv("GRAFANA_PUBLIC_URL", "http://localhost:3000"),
    }


@bp.get("/")
def home():
    return render_template("home.html")


@bp.get("/dashboard")
def dashboard():
    analyses = list_analyses(6)
    latest = get_analysis(analyses[0]["id"]) if analyses else None
    return render_template("dashboard.html", analyses=analyses, latest=latest)


@bp.get("/api/status")
def api_status():
    analyses = list_analyses(100)
    latest = get_analysis(analyses[0]["id"]) if analyses else None
    return {
        "platform": "AquaVigil",
        "mode": "synthetic-demo",
        "analysis_count": len(analyses),
        "latest": {
            "id": latest["id"],
            "created_at": latest["created_at"],
            "filename": latest["filename"],
            "status": latest["result"]["status"],
            "risk_score": latest["result"]["risk_score"],
            "record_count": latest["result"]["record_count"],
            "findings": len(latest["result"]["findings"]),
            "alert_count": len([finding for finding in latest["result"]["findings"] if finding["severity"] in ("warning", "critical")]),
        } if latest else None,
    }


@bp.get("/api/alerts")
def api_alerts():
    analyses = list_analyses(1)
    latest = get_analysis(analyses[0]["id"]) if analyses else None
    alerts = [] if not latest else [
        {"severity": finding["severity"], "title": finding["title"], "domain": finding["domain"], "reason": finding["detection_logic"], "response": finding["recommendation"]}
        for finding in latest["result"]["findings"] if finding["severity"] in ("warning", "critical")
    ]
    return {"analysis_id": latest["id"] if latest else None, "count": len(alerts), "alerts": alerts}


@bp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        item = request.files.get("evidence")
        if not item or not item.filename:
            flash("Choose a CSV or JSON evidence file.", "error")
            return redirect(url_for("main.upload"))
        if not item.filename.lower().endswith((".csv", ".json")):
            flash("Only CSV and JSON demonstration evidence are accepted.", "error")
            return redirect(url_for("main.upload"))
        payload = item.read()
        try:
            result = analyze(payload, item.filename)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            flash(str(exc), "error")
            return redirect(url_for("main.upload"))
        analysis_id = save_analysis(item.filename, digest(payload), result)
        observe(result)
        return redirect(url_for("main.analysis", analysis_id=analysis_id))
    return render_template("upload.html")


@bp.get("/analysis/<int:analysis_id>")
def analysis(analysis_id):
    item = get_analysis(analysis_id)
    if not item:
        abort(404)
    return render_template("analysis.html", item=item)


@bp.get("/report/<int:analysis_id>")
def report(analysis_id):
    item = get_analysis(analysis_id)
    if not item:
        abort(404)
    return render_template("report.html", item=item)


@bp.get("/report/<int:analysis_id>/download")
def download_report(analysis_id):
    item = get_analysis(analysis_id)
    if not item:
        abort(404)
    html = render_template("report.html", item=item, standalone=True)
    return Response(html, headers={"Content-Disposition": f"attachment; filename=aquavigil-report-{analysis_id}.html"}, mimetype="text/html")


@bp.post("/report/<int:analysis_id>/delete")
def delete_report(analysis_id):
    if not delete_analysis(analysis_id):
        abort(404)
    flash(f"Report #{analysis_id} and its stored analysis were deleted.", "success")
    return redirect(url_for("main.history"))


@bp.get("/history")
def history():
    return render_template("history.html", analyses=list_analyses(100))


@bp.get("/workspace/<section>")
def workspace(section):
    allowed = {"quality", "desalination", "security", "threats", "optimization", "assets", "devsecops", "compliance", "integrations", "architecture", "monitoring"}
    if section not in allowed:
        abort(404)
    analyses = list_analyses(1)
    latest = get_analysis(analyses[0]["id"]) if analyses else None
    # Each operational workspace keeps its own latest compatible evidence.
    # A network-log analysis must not hide previously analyzed process signals.
    if section == "quality":
        latest = _latest_for_workspace("quality", {"ph", "turbidity", "chlorine", "temperature"}) or latest
    elif section == "desalination":
        latest = _latest_for_workspace("desalination", {"pressure", "flow"}) or latest
    scan_results, scan_generated_at = None, None
    if section == "devsecops":
        root = Path(current_app.root_path).parent
        if request.args.get("run") == "1":
            scan_results = _run_devsecops_checks(root)
            scan_generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    series = latest["result"].get("series", {}) if latest else {}
    return render_template(
        "workspace.html", section=section, latest=latest, scan_results=scan_results,
        scan_generated_at=scan_generated_at,
        has_quality=any(name in series for name in ("ph", "conductivity", "turbidity", "chlorine", "salinity", "temperature")),
        has_desalination=any(name in series for name in ("pressure", "flow", "salinity", "conductivity")),
    )


@bp.get("/demo/load")
def load_demo():
    path = Path(current_app.root_path).parent / "data" / "unexpected_dosing_incident.csv"
    payload = path.read_bytes()
    result = analyze(payload, path.name)
    analysis_id = save_analysis(path.name, digest(payload), result)
    observe(result)
    return redirect(url_for("main.analysis", analysis_id=analysis_id))


@bp.get("/demo/load/<scenario>")
def load_scenario(scenario):
    samples = {
        "quality": "quality_excursion.csv",
        "desalination": "membrane_fouling.csv",
        "dosing": "unexpected_dosing_incident.csv",
        "zeek": "zeek_network_evidence.csv",
        "suricata": "suricata_alerts.json",
    }
    filename = samples.get(scenario)
    if not filename:
        abort(404)
    path = Path(current_app.root_path).parent / "data" / filename
    payload = path.read_bytes()
    result = analyze(payload, path.name)
    if scenario in ("quality", "desalination"):
        result["workspace_roles"] = [scenario]
    analysis_id = save_analysis(path.name, digest(payload), result)
    observe(result)
    return redirect(url_for("main.workspace", section="integrations" if scenario in ("zeek", "suricata") else "quality" if scenario == "quality" else "desalination" if scenario == "desalination" else "threats"))


@bp.get("/samples/<path:filename>")
def sample_file(filename):
    allowed = {"normal_operation.csv", "unexpected_dosing_incident.csv", "membrane_fouling.csv", "quality_excursion.csv", "zeek_network_evidence.csv", "suricata_alerts.json"}
    if filename not in allowed:
        abort(404)
    directory = Path(current_app.root_path).parent / "data"
    return send_from_directory(directory, filename, as_attachment=True)


@bp.get("/health")
def health():
    get_db().execute("SELECT 1").fetchone()
    analyses = list_analyses(1)
    return {
        "status": "ok",
        "mode": "synthetic-demo",
        "database": "connected",
        "latest_analysis_id": analyses[0]["id"] if analyses else None,
    }


@bp.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
