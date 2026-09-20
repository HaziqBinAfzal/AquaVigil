from pathlib import Path

from app.services.analyzer import analyze


ROOT = Path(__file__).resolve().parents[1]


def test_normal_evidence_is_stable():
    path = ROOT / "data" / "normal_operation.csv"
    result = analyze(path.read_bytes(), path.name)
    assert result["status"] == "Stable"
    assert result["risk_score"] == 0
    assert result["record_count"] == 5


def test_dosing_incident_correlates_critical_finding():
    path = ROOT / "data" / "unexpected_dosing_incident.csv"
    result = analyze(path.read_bytes(), path.name)
    assert result["status"] == "Critical"
    assert any("dosing" in finding["title"].lower() for finding in result["findings"])
    assert all(finding["detection_logic"] for finding in result["findings"])


def test_zeek_evidence_detects_unauthorized_cross_zone_connections():
    path = ROOT / "data" / "zeek_network_evidence.csv"
    result = analyze(path.read_bytes(), path.name)
    assert result["source_type"] == "Zeek connection log"
    assert result["network"]["cross_zone"] >= 1
    assert any("cross-zone" in finding["title"].lower() for finding in result["findings"])


def test_suricata_eve_alerts_are_explained():
    path = ROOT / "data" / "suricata_alerts.json"
    result = analyze(path.read_bytes(), path.name)
    assert result["source_type"] == "Suricata EVE"
    assert result["network"]["alerts"] == 2
    assert all(finding["source"] == "Suricata EVE" for finding in result["findings"])


def test_integrated_evidence_populates_process_and_network_domains():
    payload = b"timestamp,ph,turbidity,chlorine,pressure,flow,id.orig_h,id.resp_h,source_zone,dest_zone,proto,authorized\n2026-09-20T10:00:00Z,7.2,0.3,1.1,57,1150,10.0.0.7,10.0.1.8,enterprise,ot,tcp,false\n2026-09-20T10:05:00Z,9.1,1.8,0.1,75,920,10.0.0.7,10.0.1.8,enterprise,ot,tcp,true\n"
    result = analyze(payload, "integrated.csv")
    assert result["source_type"] == "Integrated water/process + Zeek connection log"
    assert {"ph", "turbidity", "chlorine", "pressure", "flow"} <= set(result["series"])
    assert result["network"]["events"] == 2
    assert result["network"]["cross_zone"] == 2
    assert any(finding["domain"] == "Water quality" for finding in result["findings"])
    assert any(finding["domain"] == "Network segmentation" for finding in result["findings"])
