import io

from app import create_app


def test_public_routes(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    client = app.test_client()
    for route in ("/", "/dashboard", "/upload", "/health", "/metrics", "/api/status", "/workspace/architecture", "/workspace/integrations", "/workspace/monitoring", "/workspace/devsecops"):
        assert client.get(route).status_code == 200

    health = client.get("/health").get_json()
    assert health["database"] == "connected"
    assert health["latest_analysis_id"] is None
    assert b"Run water-quality sample" in client.get("/workspace/quality").data
    assert b"Run desalination sample" in client.get("/workspace/desalination").data
    assert b"Run complete scan" in client.get("/workspace/devsecops").data
    architecture = client.get("/workspace/architecture").data
    assert b"EVIDENCE-TO-DECISION PIPELINE" in architecture
    assert b"Prometheus and Grafana" in architecture
    assert architecture.index(b"Overview") < architecture.index(b"Architecture") < architecture.index(b"Analyze Evidence")
    css = client.get("/static/css/live.css").data
    assert b"Dedicated protection evidence boxes" in css
    assert b".protection-evidence-scroll" in css
    assert b".architecture,.monitor-grid" not in css


def test_role_specific_samples_populate_sensor_cards(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    client = app.test_client()
    quality = client.get("/demo/load/quality", follow_redirects=True)
    assert quality.status_code == 200
    assert b"Turbidity" in quality.data and b"Chlorine" in quality.data
    desalination = client.get("/demo/load/desalination", follow_redirects=True)
    assert desalination.status_code == 200
    assert b"Pressure" in desalination.data and b"Flow" in desalination.data
    zeek = client.get("/demo/load/zeek", follow_redirects=True)
    assert zeek.status_code == 200
    assert b"Zeek connection log" in zeek.data
    # Network evidence must not replace the latest compatible process evidence.
    quality_after_zeek = client.get("/workspace/quality").data
    desalination_after_zeek = client.get("/workspace/desalination").data
    assert b"Live evidence source:" in quality_after_zeek
    assert b"quality_excursion.csv" in quality_after_zeek
    assert b"Turbidity" in quality_after_zeek
    assert b"Live evidence source:" in desalination_after_zeek
    assert b"membrane_fouling.csv" in desalination_after_zeek
    assert b"Pressure" in desalination_after_zeek


def test_integrated_upload_populates_quality_and_desalination_workspaces(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    client = app.test_client()
    payload = b"timestamp,ph,turbidity,chlorine,pressure,flow,id.orig_h,id.resp_h,source_zone,dest_zone,proto,authorized\n2026-09-20T10:00:00Z,7.2,0.3,1.1,57,1150,10.0.0.7,10.0.1.8,enterprise,ot,tcp,false\n2026-09-20T10:05:00Z,9.1,1.8,0.1,75,920,10.0.0.7,10.0.1.8,enterprise,ot,tcp,true\n"
    response = client.post(
        "/upload",
        data={"evidence": (io.BytesIO(payload), "integrated.csv")},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"INTEGRATED WATER/PROCESS + ZEEK CONNECTION LOG" in response.data
    quality = client.get("/workspace/quality").data
    desalination = client.get("/workspace/desalination").data
    security = client.get("/workspace/security").data
    assert b"integrated.csv" in quality and b"Turbidity" in quality
    assert b"integrated.csv" in desalination and b"Pressure" in desalination
    assert b"Unauthorized cross-zone connection" in security


def test_demo_creates_analysis(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    client = app.test_client()
    response = client.get("/demo/load", follow_redirects=True)
    assert response.status_code == 200
    assert b"Unauthorized chemical-dosing activity correlated" in response.data
    assert b"analysis-evidence-scroll" in response.data
    assert b"Scrollable analysis findings" in response.data
    status = client.get("/api/status").get_json()
    assert status["analysis_count"] == 1
    assert status["latest"]["status"] == "Critical"
    assert status["latest"]["alert_count"] > 0
    alerts = client.get("/api/alerts").get_json()
    assert alerts["count"] > 0
    assert alerts["alerts"][0]["reason"]

    for section in ("quality", "desalination", "security", "threats", "optimization", "assets", "compliance"):
        workspace = client.get(f"/workspace/{section}")
        assert workspace.status_code == 200
        assert b"LIVE EVIDENCE WORKSPACE" in workspace.data or section in ("security", "threats")

    security = client.get("/workspace/security").data
    threats = client.get("/workspace/threats").data
    assert b"SCADA manipulation checks" in security
    assert b"Public-health-first response workflow" in threats
    assert b"Scrollable OT and SCADA protection evidence" in security
    assert b"Scrollable Threat Center alerts" in threats
    assert b"protection-evidence-scroll" in security
    assert b"protection-evidence-scroll" in threats
    assert security != threats

    report = client.get("/report/1")
    assert b"How it was detected" in report.data
    assert b"Document navigation" in report.data
    download = client.get("/report/1/download")
    assert download.status_code == 200
    assert "attachment" in download.headers["Content-Disposition"]
    assert b"<style>" in download.data
    assert b"/static/" not in download.data

    deleted = client.post("/report/1/delete", follow_redirects=True)
    assert deleted.status_code == 200
    assert b"were deleted" in deleted.data
    assert client.get("/report/1").status_code == 404
