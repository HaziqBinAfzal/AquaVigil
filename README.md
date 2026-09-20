<div align="center">

<img src="app/static/img/aquavigil-logo.svg" alt="AquaVigil logo" width="150">

# AquaVigil

### Smart Water & Desalination Infrastructure Security Platform

**Evidence-driven water intelligence • OT/SCADA protection • explainable analysis • observability**

[![Version](https://img.shields.io/badge/version-v1.0.0-0A66C2)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?logo=python&logoColor=white)](requirements.txt)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](docker-compose.yml)
[![CI](https://github.com/HaziqBinAfzal/AquaVigil/actions/workflows/ci.yml/badge.svg)](https://github.com/HaziqBinAfzal/AquaVigil/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

> [!IMPORTANT]
> **Safety boundary:** AquaVigil is a defensive, read-only educational prototype. All bundled evidence is synthetic. It must never be connected directly to a real utility, SCADA network, controller, pump, valve, dosing system, or safety function.

## Overview

AquaVigil brings water-quality assurance, desalination insight, OT/SCADA security correlation, asset monitoring, explainable decision support, observability, and professional reporting into one workstation. The workflow begins with evidence supplied by the user; AquaVigil validates and classifies that evidence, analyzes operational and security signals, correlates findings, and presents traceable results without issuing commands to operational technology.

## Platform workflow

```mermaid
flowchart LR
    A[CSV / JSON / JSONL Evidence] --> B[Ingestion & SHA-256 Provenance]
    B --> C[Evidence-Type Detection]
    C --> D[Water & Process Analysis]
    C --> E[OT / SCADA Security]
    C --> F[Zeek / Suricata Evidence]
    D --> G[Correlation & Explainable Findings]
    E --> G
    F --> G
    G --> H[Water Quality & Desalination Views]
    G --> I[Threat Center & Asset Health]
    G --> J[Professional Reports]
    G --> K[Prometheus Metrics]
    K --> L[Grafana Dashboard]
```

## Core capabilities

| Domain | What AquaVigil demonstrates |
|---|---|
| **Evidence assurance** | CSV, JSON and JSONL ingestion, SHA-256 provenance, automatic evidence-type detection |
| **Water intelligence** | pH, conductivity, turbidity, chlorine, salinity, pressure, flow and temperature analysis |
| **Anomaly analysis** | Deterministic operating-range checks and a transparent recent-baseline anomaly model |
| **OT / SCADA protection** | Authorization, zone, connection, signature and process-context correlation |
| **Passive monitoring** | Zeek-style connection evidence and Suricata EVE-style security events |
| **Desalination insight** | Fouling, specific-energy and daily-demand decision support with visible reasoning |
| **Explainability** | Findings show observed evidence, expected condition, method, impact, source and safe response |
| **Reporting** | Report history, provenance, print/PDF workflow, HTML export and controlled deletion |
| **Observability** | Prometheus telemetry plus a provisioned Grafana water-operations dashboard |
| **Standards evidence** | Mapping to WHO water-safety concepts, EPA guidance, national water-safety requirements and NIST SP 800-82 |

## Interface

AquaVigil's workspace is organized around the operational workflow:

**Overview → Analyze Evidence → Water Quality → Desalination → Asset Health → OT / SCADA Security → Threat Center → Zeek / Suricata → Reports**

The repository includes the AquaVigil visual assets and complete responsive web interface.

## Quick start

### Windows one-click — recommended

1. Clone or download the repository.
2. Make sure Docker Desktop is installed and running.
3. Double-click `OPEN-AQUAVIGIL.vbs`.
4. AquaVigil starts its services, waits for health checks, and opens the application in your browser.

Use `START-AQUAVIGIL.cmd` when you want visible startup diagnostics. Use `STOP-AQUAVIGIL.cmd` to stop the stack.

### Docker / PowerShell

```powershell
Copy-Item .env.example .env -ErrorAction SilentlyContinue
docker compose pull prometheus grafana
docker compose up --build -d
docker compose ps
```

| Service | Local address | Default access |
|---|---|---|
| AquaVigil | `http://localhost:8000` | No application login in this prototype |
| Prometheus | `http://localhost:9090` | Local service |
| Grafana | `http://localhost:3000` | `admin` / `aquavigil` |

> [!NOTE]
> The first Docker start may download Prometheus and Grafana images. Ports can be changed in `.env` using `APP_PORT`, `PROMETHEUS_PORT`, and `GRAFANA_PORT`.

### macOS / Linux

```bash
chmod +x start-aquavigil.sh stop-aquavigil.sh
./start-aquavigil.sh
```

## Local Python development

```powershell
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q
python run.py
```

The local Python route runs the web application at `http://localhost:5000`; it does not start Prometheus or Grafana.

## Synthetic evidence library

Bundled demonstration files live in `data/` and can also be accessed from **Analyze Evidence**:

- `normal_operation.csv` — baseline operating evidence
- `unexpected_dosing_incident.csv` — dosing-related process scenario
- `quality_excursion.csv` — water-quality excursion
- `membrane_fouling.csv` — desalination/membrane scenario
- `zeek_network_evidence.csv` — passive network evidence
- `suricata_alerts.json` — IDS-style event evidence

All bundled scenarios are synthetic and are intended for safe demonstration and testing.

## Repository structure

```text
.github/             CI and dependency-update automation
app/                 Flask application, analysis engine, templates, UI and metrics
data/                Synthetic process, water, Zeek-style and Suricata evidence
docker/              Prometheus and Grafana configuration
docs/                Architecture, security, recovery, requirements and demo guidance
scripts/             Setup/support scripts
tests/               Analyzer and application tests
Dockerfile           AquaVigil application image
docker-compose.yml   AquaVigil + Prometheus + Grafana stack
```

## Documentation

| Document | Purpose |
|---|---|
| [Architecture](docs/ARCHITECTURE.md) | System structure and data flow |
| [Demonstration Guide](docs/DEMONSTRATION_GUIDE.md) | Guided project demonstration |
| [Requirement Matrix](docs/REQUIREMENT_MATRIX.md) | Requirement-to-evidence mapping |
| [Security](docs/SECURITY.md) | Defensive boundaries and security considerations |
| [Failure & Recovery](docs/FAILURE_RECOVERY.md) | Recovery and troubleshooting guidance |
| [Changelog](CHANGELOG.md) | Version history |

## Demonstration path

1. Start with the safety boundary and architecture.
2. Upload one of the synthetic evidence samples.
3. Review evidence detection, provenance and sensor/network observations.
4. Inspect explainable findings across water/process and security contexts.
5. Review desalination decision support and asset-health reasoning.
6. Generate the professional report and inspect standards evidence mapping.
7. Open Prometheus and Grafana to demonstrate observability.
8. Discuss passive monitoring, segmentation, the industrial DMZ and recovery controls.

## Testing and automation

Run the automated tests with:

```bash
pytest -q
```

GitHub Actions provides repository CI, while Dependabot tracks supported dependency updates. Docker configuration keeps the application, Prometheus and Grafana deployment reproducible.

## Design principles

AquaVigil is built around four boundaries:

- **Read-only by design:** analysis and visualization, not operational control.
- **Evidence before claims:** findings are tied to supplied evidence and provenance.
- **Explainability:** detections expose the condition and reasoning behind the finding.
- **Safe demonstration:** bundled datasets are synthetic and separated from real infrastructure.

## Limitations

AquaVigil is an educational defensive prototype. Its output is not laboratory certification, engineering approval, legal advice, formal regulatory certification, or authorization to operate critical infrastructure. Real-world deployment would require explicit authorization, secure architecture, authenticated access, independent water-quality verification, validated engineering limits, change control, and qualified operators.

## License

Released under the [MIT License](LICENSE).

---

<div align="center">

**AquaVigil v1.0.0 — defensive water intelligence with an explicit OT safety boundary.**

</div>
