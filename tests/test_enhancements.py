import json
from pathlib import Path

from app import create_app
from app.services.analyzer import analyze
from app.services.assurance import notification_draft
from app.services.trends import next_flow_projection

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_model_has_holdout_evidence_and_safe_language():
    evaluation = json.loads((ROOT / "app/models/evaluation.json").read_text())
    assert evaluation["holdout_samples"] > 0
    assert "synthetic" in evaluation["limitations"].lower() or "generated" in evaluation["limitations"].lower()
    result = analyze((ROOT / "data/normal_operation.csv").read_bytes(), "normal_operation.csv")
    assert result["ml_quality"]["model"] == "synthetic-v1"
    assert "not contamination confirmation" in result["ml_quality"]["note"]


def test_local_advisory_and_unconfigured_jurisdiction():
    path = ROOT / "data/suricata_alerts.json"
    result = analyze(path.read_bytes(), path.name)
    assert any(match["advisory_id"] == "DEMO-ICS-001" for match in result["advisory_matches"])
    assert all("SYNTHETIC" in match["source"] for match in result["advisory_matches"])
    national = next(row for row in result["standards_evidence"] if row["framework"] == "Local jurisdiction")
    assert not national["evidenced"]


def test_flow_projection_uses_later_records_as_holdout():
    result = next_flow_projection([1100 + 2*i for i in range(20)])
    assert result["available"] and result["holdout_records"] == 5
    assert result["projected_next_flow_m3_h"] > 1100
    assert not next_flow_projection([1100] * 5)["available"]


def test_restart_retains_audit_and_generates_unsent_draft(tmp_path):
    db = str(tmp_path / "persistent.db")
    app = create_app({"TESTING": True, "DATABASE": db})
    first = app.test_client().get("/demo/load")
    assert first.status_code == 302
    restarted = create_app({"TESTING": True, "DATABASE": db})
    client = restarted.test_client()
    assert client.get("/api/status").get_json()["analysis_count"] == 1
    draft = client.get("/report/1/notification-draft").get_json()
    assert draft["type"].startswith("DRAFT") and draft["recipient"].startswith("Not selected")
    audit = client.get("/report/1/audit-record").get_json()
    assert len(audit["source_sha256"]) == 64 and audit["findings"]


def test_new_capabilities_are_visible_in_relevant_workspaces(tmp_path):
    client = create_app({"TESTING": True, "DATABASE": str(tmp_path / "views.db")}).test_client()
    assert b"From quality screening to reviewable records" in client.get("/dashboard").data
    assert b"Where these monitoring values come from" in client.get("/workspace/monitoring").data
    assert b"Configured off" in client.get("/workspace/monitoring").data
    client.get("/demo/load/quality")
    assert b"Quality pattern screening" in client.get("/workspace/quality").data
    client.get("/demo/load/desalination")
    assert b"Know what the resource numbers mean" in client.get("/workspace/optimization").data
    client.get("/demo/load/suricata")
    assert b"Check the source behind a matching indicator" in client.get("/workspace/threats").data
    assert b"Keep the evidence; prepare a human-reviewed response" in client.get("/workspace/compliance").data
