from prometheus_client import Counter, Gauge


ANALYSES = Counter("aquavigil_analyses_total", "Completed evidence analyses", ["status", "source_type"])
LAST_RISK = Gauge("aquavigil_last_risk_score", "Most recent analysis risk score")
LAST_CONFIDENCE = Gauge("aquavigil_last_sensor_confidence_percent", "Most recent evidence confidence")
LAST_RECORDS = Gauge("aquavigil_last_records", "Records in the most recent analysis")
LAST_INVALID = Gauge("aquavigil_last_invalid_values", "Invalid values in the most recent analysis")
FINDINGS = Gauge("aquavigil_last_findings", "Findings in the most recent analysis", ["severity"])
SENSOR_LATEST = Gauge("aquavigil_sensor_latest", "Latest water or process sensor value", ["sensor", "unit"])
SENSOR_MEAN = Gauge("aquavigil_sensor_mean", "Mean water or process sensor value", ["sensor", "unit"])
FOULING = Gauge("aquavigil_membrane_fouling_risk_percent", "Calculated membrane fouling risk")
ENERGY = Gauge("aquavigil_specific_energy_kwh_m3", "Estimated specific energy")
DEMAND = Gauge("aquavigil_demand_forecast_m3_day", "Estimated daily demand")
NETWORK_EVENTS = Gauge("aquavigil_network_events", "Passive network events in latest analysis")
NETWORK_ALERTS = Gauge("aquavigil_network_alerts", "Suricata alerts in latest analysis")
CROSS_ZONE = Gauge("aquavigil_cross_zone_connections", "Cross-zone connections in latest analysis")
COMPLIANCE = Gauge("aquavigil_compliance_evidence", "Compliance mapping evidence state", ["framework"])


def observe(result):
    ANALYSES.labels(status=result["status"].lower(), source_type=result.get("source_type", "unknown")).inc()
    LAST_RISK.set(result["risk_score"])
    LAST_CONFIDENCE.set(result["sensor_confidence"])
    LAST_RECORDS.set(result["record_count"])
    LAST_INVALID.set(result["invalid_values"])
    for severity in ("warning", "critical"):
        FINDINGS.labels(severity=severity).set(sum(1 for finding in result["findings"] if finding["severity"] == severity))
    for sensor, values in result.get("series", {}).items():
        unit = values.get("unit", "value")
        SENSOR_LATEST.labels(sensor=sensor, unit=unit).set(values["latest"])
        SENSOR_MEAN.labels(sensor=sensor, unit=unit).set(values["mean"])
    optimization = result["optimization"]
    FOULING.set(optimization["membrane_fouling_risk"])
    ENERGY.set(optimization["specific_energy_kwh_m3"])
    DEMAND.set(optimization["demand_forecast_m3"])
    network = result.get("network", {})
    NETWORK_EVENTS.set(network.get("events", 0)); NETWORK_ALERTS.set(network.get("alerts", 0)); CROSS_ZONE.set(network.get("cross_zone", 0))
    for item in result.get("compliance", []):
        COMPLIANCE.labels(framework=item["framework"]).set(1 if item["state"] == "Evidence available" else 0)
