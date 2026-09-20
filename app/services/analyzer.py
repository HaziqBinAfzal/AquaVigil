import csv
import hashlib
import io
import json
import math
import statistics


LIMITS = {
    "ph": (6.5, 8.5, "pH units"), "conductivity": (50, 1500, "µS/cm"),
    "turbidity": (0, 1.0, "NTU"), "chlorine": (0.2, 4.0, "mg/L"),
    "salinity": (0, 0.5, "ppt"), "pressure": (2, 80, "bar"),
    "flow": (1, 5000, "m³/h"), "temperature": (2, 35, "°C"),
}
ALIASES = {"residual_chlorine": "chlorine", "temp": "temperature"}


def _records(payload, filename):
    text = payload.decode("utf-8-sig")
    if filename.lower().endswith(".json"):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return parsed
            return parsed.get("records", [parsed])
        except json.JSONDecodeError:
            return [json.loads(line) for line in text.splitlines() if line.strip()]
    return list(csv.DictReader(io.StringIO(text)))


def _flatten(record):
    flat = dict(record)
    for key in ("alert", "flow", "http", "dns"):
        if isinstance(record.get(key), dict):
            for child, value in record[key].items():
                flat[f"{key}.{child}"] = value
    return flat


def _number(record, name):
    value = record.get(name)
    if value in (None, ""):
        for alias, canonical in ALIASES.items():
            if canonical == name and record.get(alias) not in (None, ""):
                value = record[alias]
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _finding(domain, severity, title, observed, expected, logic, impact, recommendation, source):
    return {"domain": domain, "severity": severity, "title": title, "observed": observed,
            "expected": expected, "detection_logic": logic, "why_it_matters": impact,
            "evidence": observed, "recommendation": recommendation, "source": source}


def _detect_source(records):
    keys = {key for row in records for key in _flatten(row)}
    if "event_type" in keys or "alert.signature" in keys:
        return "Suricata EVE"
    if {"id.orig_h", "id.resp_h"} & keys or {"orig_bytes", "resp_bytes", "conn_state"} <= keys:
        return "Zeek connection log"
    return "Water/process telemetry"


def _is_water_record(record):
    return any(_number(record, sensor) is not None for sensor in LIMITS)


def _is_network_record(record):
    keys = set(_flatten(record))
    return bool(keys & {"event_type", "alert.signature", "id.orig_h", "id.resp_h", "src_ip", "dest_ip", "source_zone", "dest_zone", "conn_state"})


def _water_analysis(records, findings, series):
    invalid = 0
    for sensor, (low, high, unit) in LIMITS.items():
        values = [_number(row, sensor) for row in records]
        clean = [value for value in values if value is not None and math.isfinite(value)]
        invalid += len(values) - len(clean)
        if not clean:
            continue
        mean = statistics.fmean(clean)
        series[sensor] = {"latest": round(clean[-1], 2), "mean": round(mean, 2),
                          "min": round(min(clean), 2), "max": round(max(clean), 2),
                          "values": [round(value, 2) for value in clean[-24:]],
                          "range": [low, high], "unit": unit}
        breaches = [value for value in clean if value < low or value > high]
        if breaches:
            ratio = len(breaches) / len(clean)
            findings.append(_finding(
                "Water quality", "critical" if ratio >= 0.25 else "warning",
                f"{sensor.title()} outside the configured safe range",
                f"{len(breaches)} of {len(clean)} readings breached {low}–{high} {unit}; observed {min(clean):.2f}–{max(clean):.2f} {unit}.",
                f"Every valid {sensor} reading should remain between {low} and {high} {unit} for this demonstration profile.",
                "A deterministic limit check compared every parsed reading with the documented operating envelope.",
                "A sustained excursion can indicate sensor error, treatment instability, or a condition requiring independent sampling.",
                "Verify calibration, obtain an independent sample, inspect the relevant treatment stage, and follow the approved escalation procedure.",
                "AquaVigil threshold engine"))
        if len(clean) >= 4:
            baseline = clean[:-1]
            spread = statistics.pstdev(baseline)
            deviation = abs(clean[-1] - statistics.fmean(baseline))
            if spread > 0 and deviation / spread >= 3 and not breaches:
                findings.append(_finding(
                    "Behavior analytics", "warning", f"Unusual {sensor} movement",
                    f"Latest value {clean[-1]:.2f} {unit} is {deviation / spread:.1f} standard deviations from the preceding baseline.",
                    "The latest reading should remain consistent with the recent evidence baseline unless an operating change is documented.",
                    "The explainable anomaly engine built a baseline from earlier values and flagged a ≥3σ deviation.",
                    "A sudden but in-range movement can be an early indicator of drift, process transition, or manipulated telemetry.",
                    "Corroborate with an independent sensor and review operator/change records before taking action.",
                    "AquaVigil baseline engine"))
    dosing = [str(row.get("dosing_command", "")).lower() for row in records]
    authorization = [str(row.get("authorized", "true")).lower() for row in records]
    suspicious = sum(1 for command, allowed in zip(dosing, authorization)
                     if command not in ("", "none", "hold") and allowed in ("false", "0", "no"))
    if suspicious:
        findings.append(_finding(
            "OT security", "critical", "Unauthorized chemical-dosing activity correlated",
            f"{suspicious} non-hold dosing command(s) were explicitly marked unauthorized in the evidence.",
            "Chemical-dosing changes must originate from an approved OT workflow and carry valid authorization context.",
            "The correlation engine joined command intent and authorization state record by record, then checked quality context.",
            "Unauthorized dosing can create a cyber-physical public-health consequence rather than a network-only alert.",
            "Isolate the command path, preserve logs, independently verify water quality, and restore a validated controller configuration under operator authority.",
            "AquaVigil cyber-process correlation"))
    return invalid


def _network_analysis(records, source_type, findings):
    network = {"events": len(records), "alerts": 0, "denied": 0, "cross_zone": 0,
               "sources": set(), "destinations": set(), "protocols": set()}
    for raw in records:
        row = _flatten(raw)
        src = str(row.get("src_ip") or row.get("id.orig_h") or "unknown")
        dst = str(row.get("dest_ip") or row.get("id.resp_h") or "unknown")
        network["sources"].add(src); network["destinations"].add(dst)
        protocol = str(row.get("proto") or row.get("app_proto") or row.get("service") or "unknown")
        network["protocols"].add(protocol)
        signature = row.get("alert.signature")
        severity_value = row.get("alert.severity", 3)
        if signature:
            network["alerts"] += 1
            findings.append(_finding(
                "Network security", "critical" if str(severity_value) in ("1", "2") else "warning",
                f"Suricata alert: {signature}", f"{src} → {dst} over {protocol}; signature severity {severity_value}.",
                "OT traffic should match approved protocols, endpoints, and detection policy without high-priority signatures.",
                "The EVE adapter extracted the alert object, endpoints, protocol, signature, and severity.",
                "A signature match is investigative evidence; its process significance depends on asset and water-quality context.",
                "Validate the signature, inspect adjacent Zeek/process evidence, preserve the event, and contain only through approved procedures.",
                "Suricata EVE"))
        state = str(row.get("conn_state", ""))
        if state in ("REJ", "RSTO", "RSTR"):
            network["denied"] += 1
        src_zone = str(row.get("source_zone", "")).lower()
        dst_zone = str(row.get("dest_zone", "")).lower()
        allowed = str(row.get("authorized", "true")).lower() not in ("false", "0", "no")
        if src_zone and dst_zone and src_zone != dst_zone:
            network["cross_zone"] += 1
            if not allowed:
                findings.append(_finding(
                    "Network segmentation", "critical", "Unauthorized cross-zone connection",
                    f"{src} in {src_zone} attempted {protocol} communication with {dst} in {dst_zone}; authorization=false.",
                    "Cross-zone OT communication must follow the approved conduit and access policy.",
                    "The Zeek-style adapter compared source/destination zones and authorization for every connection.",
                    "Unapproved enterprise-to-OT communication can bypass the industrial DMZ and expose a control path.",
                    "Preserve the record, verify the asset owner, block through the approved firewall workflow, and investigate the identity.",
                    source_type))
    network.update({"sources": len(network["sources"]), "destinations": len(network["destinations"]),
                    "protocols": sorted(network["protocols"])})
    return network


def analyze(payload, filename):
    records = _records(payload, filename)
    if not records or not all(isinstance(record, dict) for record in records):
        raise ValueError("The file contains no analyzable evidence records.")
    water_records = [record for record in records if _is_water_record(record)]
    network_records = [record for record in records if _is_network_record(record)]
    network_source = _detect_source(network_records) if network_records else None
    if water_records and network_records:
        source_type = f"Integrated water/process + {network_source}"
    elif network_records:
        source_type = network_source
    else:
        source_type = "Water/process telemetry"
    findings, series = [], {}
    invalid = 0
    network = {"events": 0, "alerts": 0, "denied": 0, "cross_zone": 0,
               "sources": 0, "destinations": 0, "protocols": []}
    if water_records:
        invalid = _water_analysis(water_records, findings, series)
    if network_records:
        network = _network_analysis(network_records, network_source, findings)

    pressures = [_number(row, "pressure") for row in records]
    pressures = [value for value in pressures if value is not None]
    pressure_factor = max(0, (statistics.fmean(pressures) - 55) * 1.6) if pressures else 0
    quality_factor = sum(8 for finding in findings if finding["domain"] in ("Water quality", "Behavior analytics"))
    fouling = min(99, round(18 + pressure_factor + quality_factor))
    energy = round(min(6.5, 2.7 + fouling * 0.018), 2)
    flow_values = [_number(row, "flow") for row in records]
    flow_values = [value for value in flow_values if value is not None]
    demand = round(statistics.fmean(flow_values) * 24) if flow_values else 0
    risk = min(100, sum(32 if finding["severity"] == "critical" else 14 for finding in findings) + min(15, invalid))
    status = "Critical" if risk >= 60 else "Attention" if risk >= 25 else "Stable"
    expected = len(water_records) * len(LIMITS) if water_records else len(network_records) * 4
    confidence = max(40, round(100 - (invalid / max(1, expected) * 100)))
    tools = ["AquaVigil validation engine", "Explainable baseline engine"]
    if network_source and network_source.startswith("Zeek"): tools.append("Zeek log adapter")
    if network_source and network_source.startswith("Suricata"): tools.append("Suricata EVE adapter")
    return {
        "status": status, "risk_score": risk, "record_count": len(records), "invalid_values": invalid,
        "sensor_confidence": confidence, "source_type": source_type, "tools": tools,
        "series": series, "findings": findings, "network": network,
        "summary": {"headline": f"{status} evidence state with {len(findings)} explainable finding(s)",
                    "what_was_analyzed": f"{len(records)} {source_type.lower()} record(s) were parsed, validated, and correlated.",
                    "how_it_worked": "AquaVigil used deterministic operating limits, an explainable recent-baseline model, authorization checks, and network-event context. No opaque score is used without supporting evidence.",
                    "next_action": "Review the evidence details and use approved operating, laboratory, and incident-response procedures before any real-world action." if findings else "Continue evidence collection and trend monitoring; no mapped anomaly was found."},
        "optimization": {"membrane_fouling_risk": fouling, "specific_energy_kwh_m3": energy,
                         "demand_forecast_m3": demand,
                         "recommendation": "Schedule a supervised membrane inspection and review normalized pressure/flow trends." if fouling > 55 else "Continue trend monitoring within approved engineering limits.",
                         "authority": "Decision support only—engineering limits, laboratory evidence, and operator approval remain authoritative.",
                         "explanation": f"Fouling risk combines the pressure factor ({pressure_factor:.1f}) with quality/anomaly evidence ({quality_factor} points); energy rises with calculated fouling risk."},
        "incident_flow": ["Detect", "Validate", "Correlate", "Prioritize", "Respond", "Recover"],
        "compliance": [
            {"framework": "WHO Water Safety Plan", "control": "Operational monitoring", "state": "Evidence available" if series else "Not evidenced", "evidence": f"{len(series)} validated water/process signal(s)"},
            {"framework": "NIST SP 800-82 Rev. 3", "control": "OT monitoring and segmentation", "state": "Evidence available" if network["events"] else "Architecture mapping", "evidence": f"{network['events']} passive network event(s); read-only architecture"},
            {"framework": "EPA Guidelines", "control": "Detection, response, and public-health protection", "state": "Evidence available", "evidence": f"{len(findings)} documented finding(s) with safe response guidance"},
            {"framework": "National water safety regulations", "control": "Certification evidence and regulatory inspection audit trail", "state": "Evidence available" if series else "Not evidenced", "evidence": f"{len(series)} validated water/process signal(s); retained analysis report"},
        ],
    }


def digest(payload):
    return hashlib.sha256(payload).hexdigest()
