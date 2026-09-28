"""Local, versioned demonstration evidence maps and advisory matching."""
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def advisory_matches(records):
    feed = json.loads((ROOT / "data" / "water_sector_advisories.json").read_text())
    matches = []
    for item in feed["indicators"]:
        for index, row in enumerate(records):
            if item["field"] == "alert.signature":
                alert = row.get("alert", {})
                value = alert.get("signature", "") if isinstance(alert, dict) else row.get("alert.signature", "")
            else:
                value = row.get(item["field"], "")
            if item["match"].lower() in str(value).lower():
                matches.append({"row": index + 1, "advisory_id": item["id"],
                                "observed": str(value), "source": feed["source"],
                                "published": feed["published"], "action": item["action"]})
    return matches[:25]


def evidence_map(result):
    findings = result.get("findings", [])
    network = result.get("network", {})
    series = result.get("series", {})
    checks = [
        ("WHO Water Safety Plan", "Operational monitoring", bool(series), "Uploaded sensor trends and configured demo limits"),
        ("EPA water-system guidance", "Incident evidence", bool(findings), "Finding, detection reason and response advice"),
        ("NIST SP 800-82 Rev. 3", "Passive OT network visibility", bool(network.get("events")), "Exported connection and alert records"),
        ("Local jurisdiction", "Regulatory submission", False, "Jurisdiction and authority have not been configured"),
    ]
    return [{"framework": framework, "area": area, "evidenced": state, "evidence": evidence,
             "assessment": "Demonstration evidence only; no certification or legal conclusion"}
            for framework, area, state, evidence in checks]


def notification_draft(item):
    result = item["result"]
    return {"type": "DRAFT FOR HUMAN REVIEW — NOT SENT",
            "prepared_at_utc": datetime.now(timezone.utc).isoformat(),
            "source_file": item["filename"], "sha256": item["sha256"],
            "analysis_time_utc": item["created_at"], "status": result["status"],
            "observations": [{"severity": f["severity"], "title": f["title"], "observed": f["observed"]}
                             for f in result["findings"]],
            "verification": "Independent sample, calibration and authorized operator review pending",
            "recipient": "Not selected; jurisdiction and incident reporting duty require human determination",
            "public_health_action": "Follow approved water-safety procedures; no automatic notification or actuation"}
