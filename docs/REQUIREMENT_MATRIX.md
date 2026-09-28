# Topic 133 requirement-to-evidence matrix

This maps the exam brief to **running demonstration evidence** and **work still required for deployment**. All bundled scenarios and optional local sensor messages are synthetic. Without an analysis, operational pages show an empty state instead of invented plant telemetry.

| Objective | Available AquaVigil evidence | What this does not establish |
| --- | --- | --- |
| Water treatment SCADA / OT security | Read-only OT evidence views, dosing scenario and architecture diagram | No live SCADA, OpenSCADA or PLC connection |
| Network segmentation / industrial DMZ | Five-zone trust-boundary **design** and controlled-flow explanation | No plant firewall or DMZ is deployed by Docker Compose |
| Dosing manipulation / process tampering | Finding from `unexpected_dosing_incident.csv` with authorization and process context | No validated plant detector or controller command interception |
| Water quality ML / contamination | Sensor validation, thresholds and versioned scikit-learn screening trained on generated examples | No calibrated live sensors, field validation or contamination confirmation; TensorFlow is not installed |
| Membrane fouling / desalination | Heuristic fouling and energy indicators | No validated membrane lifetime forecast or live reverse-osmosis optimization |
| Water-safety threshold alerts | Findings generated from uploaded synthetic evidence | No independent laboratory result or automated public-health alert delivery |
| Cyber-physical behavioral analysis | Zeek-style CSV / Suricata-style JSON adapters and cyber-process correlation | No live Zeek/Suricata deployment or continuous plant monitoring |
| Response prioritization | Safe recommended actions, evidence preservation and an unsent notification draft | No automated containment, regulator notification or control of production |
| Sector threat intelligence | Versioned local **synthetic** water-sector advisory matches | No trusted external threat-intelligence feed |
| Resource optimization / energy | Specific-energy estimate and a next-record flow projection when enough ordered values exist | No constrained plant optimizer, tariff scheduling or distribution-network automation |
| Pump / membrane maintenance | Fouling risk and supervised inspection advice | No field-validated predictive maintenance for all equipment |
| DevSecOps | In-app scan controls, GitHub Actions tests/compilation/Bandit/pip-audit/container build and release manifest | No signed artifact, approved OT release or automated patch rollout |
| Compliance / public health | WHO/EPA/NIST evidence mapping, Audit JSON and **unsent** notification draft | No jurisdiction-specific regulatory database, certification or submitted report |
| Audit trail / reports | SQLite history, source SHA-256, downloadable reports and audit export | No qualified regulatory inspection sign-off |
| Monitoring / IoT | Prometheus/Grafana by default; optional internal MQTT publisher and InfluxDB for synthetic samples | No production sensor network or certified real-time quality assurance |

## Demonstration sequence

Open **Architecture** → upload the dosing scenario → examine **Water Quality**, **OT/SCADA Security** and **AI Optimization** → show report and audit export → show **Prometheus/Grafana** → explain human authority. For an 8–9 minute walkthrough that fits alongside the presentation, use the [demonstration guide](DEMONSTRATION_GUIDE.md).

## Scope of the listed tools and standards

- **Installed or optional in this repository:** Flask, scikit-learn, Prometheus, Grafana, optional MQTT and InfluxDB, GitHub Actions, pytest, Bandit and pip-audit.
- **Evidence formats / design references:** Zeek-style and Suricata-style exports; conceptual SCADA and DMZ boundaries.
- **Not installed as live integrations:** TensorFlow, OpenSCADA, live Zeek/Suricata sensors, external water-sector threat feeds and regulatory databases.
- **Guidance, not certification:** WHO water-safety concepts, EPA guidance, NIST SP 800-82 and jurisdiction-dependent national requirements.

**Safety boundary:** AquaVigil cannot send commands to PLCs, RTUs, pumps, valves, chemical dosing or safety functions. Qualified personnel retain operational and reporting authority.
