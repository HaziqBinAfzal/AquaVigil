# AquaVigil

**Smart Water & Desalination Infrastructure Security Platform**

AquaVigil is a defensive, read-only, evidence-driven platform for water-quality assurance, desalination insight, OT/SCADA security correlation, explainable optimization, asset monitoring, observability, and professional reporting.

> **Safety boundary:** All included evidence is synthetic. AquaVigil must never be connected directly to a real utility, SCADA network, controller, pump, valve, dosing system, or safety function.

## Working capabilities

- CSV, JSON, and JSON Lines evidence ingestion with SHA-256 provenance
- Automatic evidence-type detection for water/process telemetry, Zeek-style connection logs, Suricata EVE events, and integrated files containing multiple evidence domains
- Eight water/process signals: pH, conductivity, turbidity, chlorine, salinity, pressure, flow, and temperature
- Deterministic operating-range checks plus a transparent recent-baseline anomaly model
- Authorization, zone, connection, signature, and process-context correlation
- Every finding explains observed evidence, expected condition, detection method, impact, source, and safe response
- Fouling, specific-energy, and daily-demand decision support with visible calculation reasoning and operator guardrails
- Standards evidence mapping for WHO water safety, EPA guidelines, national water-safety regulations, and NIST SP 800-82
- Professional reports with print/PDF, HTML download, history, provenance, and delete controls
- Prometheus telemetry and a provisioned 16-panel Grafana water-operations dashboard
- Six downloadable synthetic sample datasets covering normal operation, dosing, quality, fouling, Zeek, and Suricata workflows
- Responsive water-focused interface, automated tests, architecture, failure/recovery, and demonstration documentation

## Windows one-click start — recommended

Extract the ZIP, open the inner `aquavigil` folder, and double-click `OPEN-AQUAVIGIL.vbs`. It starts Docker Desktop when needed, clears the previous demonstration session, starts all services, waits for health, and opens AquaVigil in the browser. No terminal commands are required.

Use `START-AQUAVIGIL.cmd` only when you want visible startup progress or need to troubleshoot an error.

## Manual Docker start — fallback

Open PowerShell inside the extracted `aquavigil` folder:

```powershell
Copy-Item .env.example .env -ErrorAction SilentlyContinue
docker compose pull prometheus grafana
docker compose up --build -d
docker compose ps
```

Open these services:

| Service | URL | Credentials |
|---|---|---|
| AquaVigil | <http://localhost:8000> | none |
| Prometheus | <http://localhost:9090> | none |
| Grafana | <http://localhost:3000> | `admin` / `aquavigil` |

To watch the application logs or stop the stack:

```powershell
docker compose logs -f aquavigil
docker compose down
```

The first start downloads Prometheus and Grafana, so Docker Desktop must be running and internet access must be available.

## Other launchers

- Windows diagnostics: double-click `START-AQUAVIGIL.cmd`; use `STOP-AQUAVIGIL.cmd` to stop.
- macOS/Linux: run `chmod +x start-aquavigil.sh stop-aquavigil.sh`, then `./start-aquavigil.sh`.

Ports can be changed in `.env` with `APP_PORT`, `PROMETHEUS_PORT`, and `GRAFANA_PORT`.

## Local Python development

```powershell
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q
python run.py
```

Open <http://localhost:5000>. This route runs the web application only; it does not start Prometheus or Grafana.

## Sample evidence

All sample files are in `data/` and are also downloadable from **Analyze Evidence**:

- `normal_operation.csv`
- `unexpected_dosing_incident.csv`
- `quality_excursion.csv`
- `membrane_fouling.csv`
- `zeek_network_evidence.csv`
- `suricata_alerts.json`

## Repository map

```text
app/                 Flask routes, analysis engine, database, templates, UI, and metrics
data/                Synthetic water, process, Zeek-style, and Suricata evidence
docker/              Prometheus and Grafana configuration and dashboard provisioning
docs/                Architecture, requirement mapping, security, recovery, and demo guide
tests/               Analyzer, integration, route, report, and lifecycle tests
Dockerfile           Application image
docker-compose.yml   AquaVigil + Prometheus + Grafana
```

## Demonstration sequence

1. Open the landing page and explain the read-only safety boundary.
2. Download or upload a synthetic evidence sample.
3. Show automatic multi-domain evidence detection, sensor/network observations, and explainable findings.
4. Review constrained optimization and asset-health reasoning.
5. Open the professional report and standards evidence mapping.
6. Print/save PDF, download HTML, and demonstrate controlled report deletion.
7. Open Prometheus and the provisioned Grafana dashboard to show updated metrics.
8. Explain segmentation, the industrial DMZ, passive monitoring, and recovery controls.

See [docs/DEMONSTRATION_GUIDE.md](docs/DEMONSTRATION_GUIDE.md) and [docs/REQUIREMENT_MATRIX.md](docs/REQUIREMENT_MATRIX.md).

## Important limitations

AquaVigil is an educational defensive prototype. Its results are not laboratory certification, engineering approval, legal advice, or formal regulatory certification. Real-world use requires authorization, secure deployment, authenticated access, independent water-quality verification, validated engineering limits, and qualified operators.
