# AquaVigil oral-exam demonstration

**Total exam time:** 20 minutes for the presentation **and** project. Aim for roughly 9–10 minutes of slides, 8–9 minutes in AquaVigil, and 1–2 minutes of transition or questions. Rehearse the timing with your actual laptop and Docker stack.

## Before the exam

From PowerShell in the project folder, start Docker Desktop and run:

```powershell
.\START-AQUAVIGIL.cmd
```

The visible launcher shows startup stages, service addresses and logs. Open AquaVigil from the address it prints. Default addresses are app `http://localhost:8000`, Prometheus `http://localhost:9090` and Grafana `http://localhost:3000`; the launcher may choose available ports when defaults are busy. The default Compose stack consists of AquaVigil, Prometheus and Grafana. Optional MQTT/InfluxDB simulation needs the settings in the [README](../README.md#optional-local-sensor-simulation).

Use the included synthetic files in `data/`. Prepare the app, Grafana and one report in browser tabs. Check that Grafana has readings from a completed analysis before presenting it. Synthetic or safely exported evidence must never be described as live, calibrated plant data.

## Project walkthrough: 8–9 minutes

| Time | Screen | Show and explain |
| --- | --- | --- |
| 0:00–1:00 | Overview / Architecture | AquaVigil is read-only. Walk upward from treatment to quality/safety, OT/SCADA, industrial DMZ and enterprise. This is a **design model**, not a deployed plant DMZ. |
| 1:00–3:00 | Analyze Evidence | Upload `unexpected_dosing_incident.csv`. Show evidence classification, SHA-256, dosing/process observations and findings. Explain how provenance and process context support investigation. |
| 3:00–4:00 | Water Quality | Show pH and other present sensor signals; distinguish threshold/context checks from the synthetic scikit-learn screening. A flag requests verification and does not diagnose contamination. |
| 4:00–5:00 | AI Optimization / Asset Health | Explain fouling and energy estimates. A next-record flow projection appears only when the upload contains enough ordered flow readings. It is **not** a plant optimizer or a distribution demand forecast. |
| 5:00–6:00 | OT/SCADA Security / Threat Center | Show the dosing finding, then upload `suricata_alerts.json` or `zeek_network_evidence.csv` for passive network-style evidence. The local advisory list is synthetic; there is no live threat feed or installed Zeek/Suricata sensor. |
| 6:00–7:00 | Report / Compliance | Show finding evidence, safe response, audit JSON and the **unsent** notification draft. Explain that WHO/EPA/NIST mappings organize evidence but do not certify regulatory compliance. |
| 7:00–8:00 | Monitoring / Grafana | Show application metrics and Grafana panels populated by an analysis. Point out the optional simulated MQTT/InfluxDB stream only if you actually enabled it. No dashboard reading is a certified water measurement. |
| 8:00–9:00 | DevSecOps / Close | Show the scan or CI evidence briefly, then close with the sequence: collect → validate → correlate → explain → human review. No automated OT deployment or control command occurs. |

If time is tight, keep one dosing analysis open and show the saved report and Grafana tabs. The platform has several independent sample files; one upload should not be presented as proof that every domain received relevant evidence.

## Optional deeper checks

```powershell
docker compose ps
docker compose logs --tail=50 aquavigil
```

Use `docker compose down` to stop the default stack after the exam. Do not use `docker compose down --volumes` unless you intentionally want to erase persisted local analysis records.

## Questions to prepare for

- **Why passive OT evidence?** It supplies investigative context without sending commands to controllers.
- **Why a DMZ in the architecture?** It defines an approved exchange boundary; this repository does not provision one at a water plant.
- **Why validate sensors before ML?** Calibration faults and contradictory readings can produce false alarms.
- **Does the model confirm contamination?** No. It was trained on generated examples and needs human and laboratory verification.
- **Is the optimization automatic?** No. Current indicators and a short-horizon estimate support supervised reasoning; engineering limits and operators retain authority.
- **Does the app notify regulators?** No. It produces an unsent draft for qualified review.
- **What would production use require?** Site-specific authorization, segmentation, calibrated sensors, field validation, authenticated access, secure transfer, resilience and formal change control.
