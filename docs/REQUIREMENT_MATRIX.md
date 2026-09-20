# Smart water security requirement-to-feature matrix

Operational pages are populated from the latest stored synthetic evidence analysis. Without an analysis, AquaVigil shows an explicit empty state rather than invented live plant telemetry.

| Official objective | AquaVigil evidence | Demonstration |
|---|---|---|
| Water-treatment SCADA and OT security | Five-zone architecture, passive evidence model, command-path finding | Open Architecture, then load dosing incident |
| Network segmentation and industrial DMZ | Enterprise/SOC → DMZ → OT/SCADA → Safety/Quality → Treatment | Explain controlled flows and absent direct enterprise-to-PLC path |
| Chemical dosing/process manipulation detection | Correlates `dosing_command` with authorization and quality evidence | Run `unexpected_dosing_incident.csv` |
| ML-assisted quality and contamination analysis | Eight-sensor validation, threshold/baseline signals, confidence score | Inspect sensor cards and evidence findings |
| Fouling and process optimization | Membrane-fouling risk and specific-energy estimate | Open AI Optimization and analysis result |
| Water-safety alerts | Warning/critical findings with evidence and safe actions | Review correlated findings |
| Cyber-physical behavioral analysis | Network/controller/identity/process correlation model | Explain Detect → Correlate → Prioritize → Respond |
| Public-health-first response | Contain, independently verify, restore validated state, preserve evidence | Use incident report |
| Demand and energy optimization | Demonstration demand forecast and energy indicator | Explain constrained decision-support boundary |
| Predictive maintenance | Fouling risk and supervised inspection recommendation | Open Asset Health |
| DevSecOps | In-browser pytest, compilation, Bandit, and pip-audit execution; pinned dependencies; Docker build | Click **Run complete scan** and inspect current evidence |
| Compliance/reporting | HTML report with WHO/EPA/NIST demonstration mappings | Open report; state that mapping is not certification |
| Audit trail | SQLite history plus evidence hash | Open Reports & History |
| Monitoring | Prometheus metrics and provisioned Grafana dashboard | Open ports 9090 and 3000 |
| Open-source passive monitoring | Zeek-style CSV and Suricata EVE JSON adapters with preserved source context | Upload both included network samples |
| Explainable analytics | Observed, expected, method, impact, source, and safe response for each finding | Open any analysis or report |
| Report lifecycle | Print/save PDF, HTML download, history, and confirmed deletion | Open Reports & History |
| Live observability | Risk, confidence, sensors, findings, network, optimization, and standards metrics | Open the 16-panel Grafana dashboard |

## Explicit boundaries

- All supplied evidence is synthetic and labeled as such.
- The application is read-only and has no PLC, RTU, SCADA, pump, valve, dosing, or utility command interface.
- Quality and optimization results are educational decision support, not laboratory results or engineering control instructions.
- Compliance entries are demonstration mappings, not certification or legal claims.
