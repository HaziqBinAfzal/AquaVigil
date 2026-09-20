import json
import sqlite3
from pathlib import Path

from flask import current_app, g


SCHEMA = """
CREATE TABLE IF NOT EXISTS analyses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  filename TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  status TEXT NOT NULL,
  risk_score INTEGER NOT NULL,
  result_json TEXT NOT NULL
);
"""


def get_db():
    if "db" not in g:
        path = Path(current_app.config["DATABASE"])
        path.parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app, reset=False):
    path = Path(app.config["DATABASE"])
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    if reset:
        db.execute("DELETE FROM analyses")
        db.execute("DELETE FROM sqlite_sequence WHERE name = 'analyses'")
        db.commit()
    db.close()
    app.teardown_appcontext(close_db)


def save_analysis(filename, sha256, result):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO analyses(filename, sha256, status, risk_score, result_json) VALUES (?, ?, ?, ?, ?)",
        (filename, sha256, result["status"], result["risk_score"], json.dumps(result)),
    )
    db.commit()
    return cursor.lastrowid


def list_analyses(limit=20):
    return get_db().execute(
        "SELECT id, created_at, filename, sha256, status, risk_score FROM analyses ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()


def get_analysis(analysis_id):
    row = get_db().execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    if not row:
        return None
    item = dict(row)
    item["result"] = _normalize_result(json.loads(item.pop("result_json")))
    return item


def delete_analysis(analysis_id):
    db = get_db()
    cursor = db.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    db.commit()
    return cursor.rowcount > 0


def _normalize_result(result):
    """Keep reports created by earlier AquaVigil versions readable."""
    result.setdefault("source_type", "Water/process telemetry")
    result.setdefault("workspace_roles", [])
    result.setdefault("tools", ["AquaVigil validation engine"])
    result.setdefault("network", {"events": 0, "alerts": 0, "denied": 0, "cross_zone": 0, "sources": 0, "destinations": 0, "protocols": []})
    result.setdefault("summary", {
        "headline": f"{result.get('status', 'Unknown')} evidence state with {len(result.get('findings', []))} finding(s)",
        "what_was_analyzed": f"{result.get('record_count', 0)} stored water/process record(s) were analyzed.",
        "how_it_worked": "AquaVigil applied documented operating limits and cyber-process correlation rules.",
        "next_action": "Review the stored evidence and follow approved operating and response procedures.",
    })
    for sensor, values in result.get("series", {}).items():
        values.setdefault("unit", {"ph": "pH units", "conductivity": "µS/cm", "turbidity": "NTU", "chlorine": "mg/L", "salinity": "ppt", "pressure": "bar", "flow": "m³/h", "temperature": "°C"}.get(sensor, "value"))
    for finding in result.get("findings", []):
        finding.setdefault("observed", finding.get("evidence", "Stored evidence finding"))
        finding.setdefault("expected", "The signal or action should remain within its approved operating and authorization context.")
        finding.setdefault("detection_logic", "AquaVigil applied the stored threshold or cyber-process correlation rule.")
        finding.setdefault("why_it_matters", "The condition may affect water quality, process resilience, or OT security and requires review.")
        finding.setdefault("source", "AquaVigil legacy analysis")
    optimization = result.setdefault("optimization", {})
    optimization.setdefault("explanation", "This stored result predates detailed calculation explanations; rerun the supplied evidence for the expanded model.")
    optimization.setdefault("authority", "Decision support only—engineering limits, laboratory evidence, and operator approval remain authoritative.")
    for item in result.get("compliance", []):
        item.setdefault("control", "Evidence mapping")
    result.setdefault("incident_flow", ["Detect", "Validate", "Correlate", "Prioritize", "Respond", "Recover"])
    return result
