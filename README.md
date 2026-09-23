<p align="center">
  <img src="app/static/img/aquavigil-logo.svg" alt="AquaVigil Logo" width="210">
</p>

<h1 align="center">💧 AquaVigil</h1>

<h3 align="center">Smart Water & Desalination Infrastructure Security Platform</h3>

<p align="center">
  <strong>Defensive · Read-Only · Evidence-Driven · Explainable · Observable</strong>
</p>

<p align="center">
  <strong>Evidence First. Water Intelligence Explained.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Backend-000000" alt="Flask">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED" alt="Docker">
  <img src="https://img.shields.io/badge/Prometheus-Monitoring-E6522C" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-Visualization-F46800" alt="Grafana">
  <img src="https://github.com/HaziqBinAfzal/AquaVigil/actions/workflows/ci.yml/badge.svg" alt="CI">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Release-v1.0.0-0A66C2" alt="Version">
</p>

<p align="center">
  <strong>v1.0.0 · Educational Defensive Prototype · Human-in-the-Loop</strong>
</p>

---

## Overview

**AquaVigil** is a defensive water-intelligence and OT/SCADA security workstation designed to transform synthetic or safely exported water-quality, desalination, process, asset, and cybersecurity evidence into traceable defensive intelligence.

Instead of treating operational-process observations and cybersecurity evidence as completely separate problems, AquaVigil brings them into one evidence-driven analytical workflow.

The platform can:

* validate and normalize supplied evidence;
* calculate SHA-256 provenance;
* identify supported evidence types;
* analyze water-quality and desalination observations;
* provide asset-health context;
* analyze passive OT/SCADA security evidence;
* interpret Zeek-style and Suricata-style evidence;
* correlate cyber and process observations;
* generate explainable findings;
* preserve analysis and report history;
* generate professional reports;
* expose application metrics to Prometheus;
* visualize supported telemetry through Grafana.

AquaVigil ends at **analysis, explanation, reporting, and human review**.

It does **not** control industrial infrastructure.

---

## Navigation

[Why AquaVigil](#why-aquavigil) ·
[Core Capabilities](#core-capabilities) ·
[Evidence Workflow](#evidence-processing-architecture) ·
[Architecture](#platform-architecture) ·
[Intelligence Domains](#intelligence-domains) ·
[Correlation](#cyber-process-correlation) ·
[Workspaces](#platform-workspaces) ·
[Safety](#otscada-defensive-architecture) ·
[Observability](#docker--observability-architecture) ·
[Quick Start](#quick-start) ·
[Testing](#developer-setup--testing) ·
[Documentation](#documentation)

---

# Why AquaVigil?

Water and desalination infrastructure combines two important realities:

**physical-process behavior** and **cybersecurity behavior**.

Looking at only one side can remove important context.

A process observation may deserve additional attention when relevant cybersecurity evidence appears at the same time. Likewise, a network or IDS event may become more meaningful when process, asset, or water-quality evidence provides supporting context.

AquaVigil therefore follows an **evidence-to-decision-support** model.

```mermaid
flowchart LR

    subgraph PROCESS["PROCESS & OPERATIONAL EVIDENCE"]
        direction TB
        W["Water Quality"]
        D["Desalination"]
        A["Asset Health"]
        P["Process Conditions"]
    end

    subgraph CYBER["CYBERSECURITY EVIDENCE"]
        direction TB
        Z["Zeek-Style Evidence"]
        S["Suricata-Style Evidence"]
        N["Network Context"]
        AU["Authorization Context"]
    end

    CORR["CYBER-PROCESS<br/>CORRELATION"]

    FIND["EXPLAINABLE<br/>FINDING"]

    REPORT["REPORTING &<br/>AUDIT CONTEXT"]

    HUMAN["HUMAN REVIEW<br/>Verification & Decision Support"]

    W --> CORR
    D --> CORR
    A --> CORR
    P --> CORR

    Z --> CORR
    S --> CORR
    N --> CORR
    AU --> CORR

    CORR --> FIND
    FIND --> REPORT
    REPORT --> HUMAN
```

The objective is not simply to display an alert.

AquaVigil is designed to help answer:

* What was observed?
* Which evidence supports the finding?
* What condition was expected?
* How was the observation detected?
* Are cyber and process observations related?
* What may require human review?
* What is a safe next step?
* Who retains operational authority?

---

# Core Capabilities

| Capability                   |          Support         |
| ---------------------------- | :----------------------: |
| CSV evidence ingestion       |             ✅            |
| JSON evidence ingestion      |             ✅            |
| JSONL evidence ingestion     |             ✅            |
| File validation              |             ✅            |
| Evidence normalization       |             ✅            |
| SHA-256 provenance           |             ✅            |
| Evidence-type detection      |             ✅            |
| Water-quality analysis       |             ✅            |
| Desalination intelligence    |             ✅            |
| Asset-health reasoning       |             ✅            |
| Passive OT/SCADA analysis    |             ✅            |
| Zeek-style network evidence  |             ✅            |
| Suricata-style IDS evidence  |             ✅            |
| Cyber-process correlation    |             ✅            |
| Explainable findings         |             ✅            |
| Professional reporting       |             ✅            |
| Analysis/report history      |             ✅            |
| Prometheus metrics           |             ✅            |
| Grafana visualization        |             ✅            |
| Docker Compose deployment    |             ✅            |
| Automated testing            |             ✅            |
| GitHub Actions CI            |             ✅            |
| Dependency maintenance       |             ✅            |


---

# Evidence Processing Architecture

AquaVigil follows a traceable evidence-processing pipeline.

Supported evidence enters through a controlled ingestion path before being routed to the relevant analytical domain.

```mermaid
flowchart TB

    SOURCE["SUPPORTED EVIDENCE<br/>CSV / JSON / JSONL"]

    subgraph INTAKE["INGESTION & VALIDATION"]
        direction LR

        VALIDATE["Input & File<br/>Validation"]
        PARSE["Structured<br/>Parsing"]
        NORMALIZE["Evidence<br/>Normalization"]
        REJECT["Safe<br/>Rejection"]

        VALIDATE --> PARSE
        PARSE --> NORMALIZE
        VALIDATE -->|Invalid| REJECT
    end

    subgraph PROVENANCE["PROVENANCE & CLASSIFICATION"]
        direction LR

        HASH["SHA-256<br/>Fingerprint"]
        META["Evidence<br/>Metadata"]
        CLASS["Evidence-Type<br/>Classification"]

        HASH --> META
        HASH --> CLASS
    end

    subgraph ROUTING["ANALYTICAL ROUTING"]
        direction LR

        WATER["Water Quality<br/>Analysis"]
        DESAL["Desalination<br/>Analysis"]
        ASSET["Asset Health<br/>Reasoning"]
        OT["OT / SCADA<br/>Analysis"]
        NET["Network / IDS<br/>Analysis"]
    end

    subgraph ANALYTICAL["ANALYTICAL CONTEXT"]
        direction LR

        OBS["Observed<br/>Evidence"]
        EXPECT["Expected<br/>Condition"]
        METHOD["Detection<br/>Method"]
        IMPACT["Potential<br/>Impact"]
    end

    CORR["CYBER-PROCESS<br/>CORRELATION"]

    FIND["EXPLAINABLE<br/>FINDING"]

    OUTPUT["REPORT &<br/>AUDIT RECORD"]

    REVIEW["HUMAN REVIEW"]

    SOURCE --> VALIDATE
    NORMALIZE --> HASH

    CLASS --> WATER
    CLASS --> DESAL
    CLASS --> ASSET
    CLASS --> OT
    CLASS --> NET

    WATER --> OBS
    DESAL --> OBS
    ASSET --> OBS
    OT --> OBS
    NET --> OBS

    WATER --> CORR
    DESAL --> CORR
    ASSET --> CORR
    OT --> CORR
    NET --> CORR

    OBS --> FIND
    EXPECT --> FIND
    METHOD --> FIND
    IMPACT --> FIND
    CORR --> FIND

    FIND --> OUTPUT
    OUTPUT --> REVIEW
```

### Evidence provenance

SHA-256 provenance maintains a traceable relationship between the supplied evidence and the analysis produced from it.

```text
Original Evidence
       ↓
SHA-256 Fingerprint
       ↓
Evidence Classification
       ↓
Analysis
       ↓
Findings
       ↓
Report
```

This improves reproducibility and helps identify which supplied evidence produced a particular analytical result.

Evidence remains **input for analysis**.

It is not automatically treated as proof that a real-world incident occurred.

---

# Platform Architecture

The AquaVigil platform is organized into evidence, ingestion, analysis, intelligence, persistence, observability, and human-review layers.

```mermaid
flowchart TB

    subgraph SOURCES["EVIDENCE SOURCES"]
        direction LR

        WQ["Water Quality<br/>Evidence"]
        DS["Desalination<br/>Evidence"]
        AH["Asset Health<br/>Evidence"]
        ZK["Zeek-Style<br/>Network Evidence"]
        SR["Suricata-Style<br/>IDS Evidence"]
    end

    subgraph INGEST["EVIDENCE INGESTION"]
        direction LR

        VAL["Validation"]
        PARSE["Parsing &<br/>Normalization"]
        HASH["SHA-256<br/>Provenance"]
        TYPE["Evidence-Type<br/>Classification"]

        VAL --> PARSE
        PARSE --> HASH
        HASH --> TYPE
    end

    subgraph ENGINE["ANALYSIS ENGINE"]
        direction LR

        WATER["Water Quality<br/>Analysis"]
        DESAL["Desalination<br/>Intelligence"]
        ASSET["Asset Health<br/>Reasoning"]
        OT["OT / SCADA<br/>Security Analysis"]
        NETWORK["Network / IDS<br/>Analysis"]
    end

    subgraph INTEL["INTELLIGENCE LAYER"]
        direction LR

        CONTEXT["Evidence &<br/>Context Mapping"]
        CORR["Cyber-Process<br/>Correlation"]
        FIND["Explainable<br/>Findings"]

        CONTEXT --> FIND
        CORR --> FIND
    end

    subgraph OUTPUT["REPORTING & PERSISTENCE"]
        direction LR

        REPORT["Professional<br/>Reports"]
        HISTORY["Analysis / Report<br/>History"]
        DB["SQLite<br/>Persistence"]

        REPORT --> DB
        HISTORY --> DB
    end

    subgraph OBS["OBSERVABILITY"]
        direction LR

        METRIC["Application<br/>Metrics"]
        PROM["Prometheus"]
        GRAF["Grafana"]

        METRIC --> PROM
        PROM --> GRAF
    end

    HUMAN["HUMAN REVIEW<br/>Verification & Decision Support"]

    WQ --> VAL
    DS --> VAL
    AH --> VAL
    ZK --> VAL
    SR --> VAL

    TYPE --> WATER
    TYPE --> DESAL
    TYPE --> ASSET
    TYPE --> OT
    TYPE --> NETWORK

    WATER --> CONTEXT
    DESAL --> CONTEXT
    ASSET --> CONTEXT
    OT --> CONTEXT
    NETWORK --> CONTEXT

    WATER --> CORR
    DESAL --> CORR
    ASSET --> CORR
    OT --> CORR
    NETWORK --> CORR

    FIND --> REPORT
    FIND --> HISTORY
    FIND --> METRIC

    REPORT --> HUMAN
    HISTORY --> HUMAN
```

### Architecture Principle

> **Evidence enters AquaVigil. Intelligence leaves AquaVigil. Industrial commands do not.**

The README provides the high-level architecture.

Detailed component and trust-boundary architecture is maintained in:

[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

---

# Intelligence Domains

## Water Quality

Supported evidence can contain observations involving:

* pH;
* conductivity;
* turbidity;
* chlorine;
* salinity;
* temperature;
* pressure;
* flow.

AquaVigil can compare supported observations against expected analytical conditions and generate evidence-backed findings.

It does not replace laboratory verification or qualified engineering judgment.

---

## Desalination Intelligence

The desalination workspace supports reasoning involving:

* membrane indicators;
* fouling observations;
* feed and process conditions;
* specific-energy indicators;
* demand-oriented analysis;
* operational trends;
* visible decision-support reasoning.

The objective is to expose **why** an observation exists instead of presenting only a status label.

---

## Asset Health

Asset-related evidence provides additional context for:

* process anomalies;
* water-quality observations;
* desalination findings;
* cybersecurity correlation.

Asset-health output is evidence-based decision support.

It does not independently certify the physical condition of real equipment.

---

## OT / SCADA Security

AquaVigil can analyze supplied defensive evidence involving:

* network zones;
* connection context;
* authorization observations;
* security signatures;
* process context;
* asset context;
* passive network evidence;
* security events.

Its architecture assumes **passive or safely exported evidence**.

---

## Zeek & Suricata

### Zeek-style evidence

Example:

```text
data/zeek_network_evidence.csv
```

Supported evidence can contribute:

* source and destination context;
* connection behavior;
* protocols;
* services;
* communication patterns.

### Suricata-style evidence

Example:

```text
data/suricata_alerts.json
```

Supported evidence can contribute:

* IDS alerts;
* signature context;
* event metadata;
* network-security observations.

These inputs contribute to defensive analysis and correlation.

They do not provide AquaVigil with active network or industrial-control capability.

---

# Cyber-Process Correlation

Cyber-process correlation is one of AquaVigil's central analytical concepts.

Instead of viewing process and cybersecurity evidence independently, the platform can bring supported evidence domains into a combined context.

```mermaid
flowchart TB

    subgraph PROCESS["PROCESS & OPERATIONAL EVIDENCE"]
        direction LR

        WATER["Water Quality<br/>Observations"]
        DESAL["Desalination<br/>Indicators"]
        ASSET["Asset Health<br/>Context"]
        PROC["Process<br/>Conditions"]
    end

    subgraph CYBER["CYBERSECURITY EVIDENCE"]
        direction LR

        ZEEK["Zeek-Style<br/>Connections"]
        SURI["Suricata-Style<br/>Alerts"]
        AUTH["Authorization<br/>Context"]
        ZONE["Network / Zone<br/>Context"]
    end

    subgraph CORRELATION["CORRELATION ENGINE"]
        direction LR

        TIME["Temporal<br/>Relationship"]
        ASSETMAP["Asset / Evidence<br/>Relationship"]
        PROCESSMAP["Process<br/>Relationship"]
        CYBERMAP["Cybersecurity<br/>Relationship"]
    end

    COMBINED["COMBINED<br/>EVIDENCE CONTEXT"]

    subgraph EXPLANATION["EXPLAINABLE FINDING"]
        direction LR

        OBS["Observed<br/>Evidence"]
        EXP["Expected<br/>Condition"]
        DET["Detection<br/>Method"]
        IMP["Potential<br/>Impact"]
        RESP["Safe Review<br/>Guidance"]
    end

    REVIEW["HUMAN REVIEW"]

    WATER --> TIME
    DESAL --> PROCESSMAP
    ASSET --> ASSETMAP
    PROC --> PROCESSMAP

    ZEEK --> TIME
    SURI --> CYBERMAP
    AUTH --> CYBERMAP
    ZONE --> ASSETMAP

    TIME --> COMBINED
    ASSETMAP --> COMBINED
    PROCESSMAP --> COMBINED
    CYBERMAP --> COMBINED

    COMBINED --> OBS
    COMBINED --> EXP
    COMBINED --> DET
    COMBINED --> IMP
    COMBINED --> RESP

    OBS --> REVIEW
    EXP --> REVIEW
    DET --> REVIEW
    IMP --> REVIEW
    RESP --> REVIEW
```

This allows AquaVigil to explain not only **what was observed**, but also **why the observation may deserve human review**.

---

# Explainable Findings

AquaVigil avoids treating unexplained alert scores as final conclusions.

A supported finding can expose:

```text
Observed Evidence
Expected Condition
Detection Method
Potential Impact
Evidence Source
Safe Response
Provenance
```

The platform is therefore designed to help answer:

**What happened?**

**Why was it detected?**

**Which evidence supports it?**

**What should be reviewed next?**

A finding remains an analytical result.

It does not automatically prove a real-world attack, equipment failure, or water-quality incident.

---

# Platform Workspaces

| Workspace               | Purpose                                                     |
| ----------------------- | ----------------------------------------------------------- |
| **Overview**            | High-level platform, evidence, analysis, and security state |
| **Analyze Evidence**    | Upload, validate, classify, hash, and analyze evidence      |
| **Water Quality**       | Water-quality and process observations                      |
| **Desalination**        | Membrane, energy, demand, and process reasoning             |
| **Asset Health**        | Evidence-based equipment and asset context                  |
| **OT / SCADA Security** | Passive industrial-security analysis                        |
| **Threat Center**       | Security findings and correlated context                    |
| **Zeek / Suricata**     | Passive network and IDS evidence                            |
| **Reports**             | Explainable reporting and audit history                     |

---

# Example Analysis Journey

A typical demonstration can begin with:

```text
data/unexpected_dosing_incident.csv
```

The evidence then moves through the analytical architecture:

```mermaid
flowchart LR

    FILE["SUPPLIED<br/>EVIDENCE"]

    VALIDATE["VALIDATE &<br/>NORMALIZE"]

    PROV["PROVENANCE &<br/>CLASSIFICATION"]

    ANALYZE["DOMAIN<br/>ANALYSIS"]

    CORR["CYBER-PROCESS<br/>CORRELATION"]

    FIND["EXPLAINABLE<br/>FINDING"]

    REPORT["REPORT &<br/>AUDIT RECORD"]

    HUMAN["HUMAN<br/>REVIEW"]

    FILE --> VALIDATE
    VALIDATE --> PROV
    PROV --> ANALYZE
    ANALYZE --> CORR
    CORR --> FIND
    FIND --> REPORT
    REPORT --> HUMAN
```

The important distinction is:

```text
Detection ≠ Conclusion

Finding ≠ Authorized Action
```

AquaVigil provides evidence, explanation, and context.

Operational decisions remain outside the platform.

---

# OT/SCADA Defensive Architecture

AquaVigil deliberately separates analytical capability from industrial control.

The following blueprint shows the intended defensive relationship between conceptual OT infrastructure, controlled evidence transfer, AquaVigil, and human review.

```mermaid
flowchart TB

    subgraph ENTERPRISE["ENTERPRISE / ANALYST ZONE"]
        direction LR

        ANALYST["Security / Engineering<br/>Analyst"]
        REPORT["AquaVigil<br/>Reports & Findings"]
    end

    subgraph DMZ["INDUSTRIAL DMZ / CONTROLLED TRANSFER"]
        direction LR

        EXPORT["Safely Exported<br/>Evidence"]
        GATE["Controlled Evidence<br/>Transfer Boundary"]
    end

    subgraph OT["OT / SCADA ENVIRONMENT — CONCEPTUAL"]
        direction LR

        HMI["HMI"]
        SCADA["SCADA Server"]
        HIST["Historian /<br/>Evidence Source"]
        PLC["PLC / RTU"]
        SENSOR["Sensors /<br/>Instrumentation"]
    end

    subgraph PROCESS["PHYSICAL PROCESS — CONCEPTUAL"]
        direction LR

        PUMP["Pumps"]
        VALVE["Valves"]
        DOSING["Chemical Dosing"]
        TREAT["Treatment /<br/>Desalination"]
    end

    subgraph AQUA["AQUAVIGIL — READ-ONLY ANALYTICAL ZONE"]
        direction LR

        INGEST["Evidence<br/>Ingestion"]
        ANALYZE["Defensive<br/>Analysis"]
        CORR["Cyber-Process<br/>Correlation"]
        FIND["Explainable<br/>Findings"]

        INGEST --> ANALYZE
        ANALYZE --> CORR
        CORR --> FIND
    end

    SENSOR --> PLC
    PLC --> SCADA
    HMI --> SCADA
    SCADA --> HIST

    PLC --> PUMP
    PLC --> VALVE
    PLC --> DOSING
    PLC --> TREAT

    HIST --> EXPORT
    EXPORT --> GATE
    GATE --> INGEST

    FIND --> REPORT
    REPORT --> ANALYST

    BLOCK["NO CONTROL INTERFACE<br/>No PLC / SCADA / Pump / Valve / Dosing Commands"]

    AQUA -. "CONTROL PATH INTENTIONALLY ABSENT" .-> BLOCK
```

The OT and physical-process components shown above provide **conceptual architectural context**.

They do not represent a real facility topology.

### AquaVigil safety boundary

```text
Observe
   ↓
Validate
   ↓
Analyze
   ↓
Correlate
   ↓
Explain
   ↓
Report
   ↓
Human Review
   ↓
STOP
```

AquaVigil has no operational path for:

```text
PLC manipulation
SCADA write operations
Pump-control commands
Valve-control commands
Chemical-dosing commands
Process setpoint changes
Safety-function manipulation
Autonomous operational response
```

---

# Docker & Observability Architecture

AquaVigil v1.0.0 uses a compact Docker Compose environment containing the application, Prometheus, and Grafana.

```mermaid
flowchart TB

    USER["USER / BROWSER"]

    subgraph HOST["LOCAL HOST"]

        subgraph COMPOSE["DOCKER COMPOSE ENVIRONMENT"]

            subgraph APP["AQUAVIGIL SERVICE"]
                direction TB

                WEB["Flask Application<br/>Container Port 5000"]
                HEALTH["Health Endpoint<br/>/health"]
                METRICS["Metrics Endpoint<br/>/metrics"]
                DATA["Persistent Application<br/>Data Volume"]

                WEB --> HEALTH
                WEB --> METRICS
                WEB --> DATA
            end

            subgraph MONITORING["OBSERVABILITY SERVICES"]
                direction LR

                PROM["Prometheus<br/>Port 9090"]
                GRAF["Grafana<br/>Port 3000"]

                PROM -->|"Datasource"| GRAF
            end

        end
    end

    USER -->|"localhost:8000"| WEB

    PROM -->|"Scrape /metrics"| METRICS

    USER -->|"localhost:9090"| PROM
    USER -->|"localhost:3000"| GRAF
```

This provides a clear separation between:

**Application**

```text
AquaVigil
```

**Metrics collection**

```text
Prometheus
```

**Visualization**

```text
Grafana
```

Monitoring remains separate from operational control.

---

## Default Services

| Service            | URL                             |
| ------------------ | ------------------------------- |
| AquaVigil          | `http://localhost:8000`         |
| Prometheus         | `http://localhost:9090`         |
| Prometheus Targets | `http://localhost:9090/targets` |
| Grafana            | `http://localhost:3000`         |

Default Grafana credentials:

```text
Username: admin
Password: aquavigil
```

---

# Quick Start

## Requirements

Install:

* Docker Desktop;
* Docker Compose v2;
* Git;
* Windows 10/11;
* a modern browser.

Clone AquaVigil:

```bash
git clone https://github.com/HaziqBinAfzal/AquaVigil.git
cd AquaVigil
```

---

## Windows — Recommended

Start **Docker Desktop** and wait for the Docker engine to become ready.

Then double-click:

```text
OPEN-AQUAVIGIL.vbs
```

For visible startup diagnostics:

```text
START-AQUAVIGIL.cmd
```

Or use PowerShell:

```powershell
.\start-aquavigil.ps1
```

The launcher prepares the environment, starts the Docker Compose stack, waits for AquaVigil, and opens the application.

---

# Manual Docker Deployment

Start the complete stack:

```bash
docker compose up --build -d
```

Check container status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop AquaVigil:

```bash
docker compose down
```

The v1.0.0 Compose deployment intentionally remains small:

```text
AquaVigil
Prometheus
Grafana
```

---

# Synthetic Evidence Library

Bundled demonstration evidence is stored in:

```text
data/
```

| File                             | Scenario                         |
| -------------------------------- | -------------------------------- |
| `normal_operation.csv`           | Baseline operating evidence      |
| `unexpected_dosing_incident.csv` | Dosing-related process scenario  |
| `quality_excursion.csv`          | Water-quality excursion          |
| `membrane_fouling.csv`           | Desalination / membrane scenario |
| `zeek_network_evidence.csv`      | Passive network evidence         |
| `suricata_alerts.json`           | IDS-style event evidence         |

All bundled scenarios are **synthetic** and intended for safe education, demonstration, development, and testing.

---

# Technology Stack

| Layer                  | Technology                 |
| ---------------------- | -------------------------- |
| Application            | Python 3.12+               |
| Backend                | Flask                      |
| Frontend               | HTML / CSS / JavaScript    |
| Persistence            | SQLite                     |
| Analysis               | Python analytical services |
| Evidence               | CSV / JSON / JSONL         |
| Containerization       | Docker                     |
| Orchestration          | Docker Compose             |
| Metrics                | Prometheus                 |
| Visualization          | Grafana                    |
| Testing                | Pytest                     |
| CI                     | GitHub Actions             |
| Dependency Maintenance | Dependabot                 |
| Version Control        | Git / GitHub               |

---

# Developer Setup & Testing

Docker is recommended for the complete demonstration environment.

For local Python development:

### 1. Create the environment

```powershell
py -3.12 -m venv .venv
```

### 2. Allow activation for the current PowerShell session

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

### 3. Activate

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Run tests

```powershell
pytest -q
```

### 6. Start AquaVigil

```powershell
python run.py
```

The local Python development route runs at:

```text
http://localhost:5000
```

> Direct Python development does not automatically start Prometheus or Grafana.

---

# DevSecOps Pipeline

AquaVigil includes automated repository validation and dependency maintenance.

```mermaid
flowchart LR

    DEV["DEVELOPMENT<br/>CHANGE"]

    GIT["GIT<br/>COMMIT"]

    REPO["GITHUB<br/>REPOSITORY"]

    subgraph CI["CI PIPELINE"]
        direction TB

        BUILD["Environment<br/>Preparation"]
        TEST["Automated<br/>Tests"]
        VALIDATE["Repository<br/>Validation"]

        BUILD --> TEST
        BUILD --> VALIDATE
    end

    GATE{"QUALITY<br/>GATE"}

    PASS["VALIDATED<br/>CHANGE"]

    FIX["FIX &<br/>RE-TEST"]

    DEV --> GIT
    GIT --> REPO
    REPO --> BUILD

    TEST --> GATE
    VALIDATE --> GATE

    GATE -->|Pass| PASS
    GATE -->|Fail| FIX

    FIX --> DEV
```

CI workflow:

```text
.github/workflows/ci.yml
```

Dependency configuration:

```text
.github/dependabot.yml
```

---

# Repository Structure

```text
AquaVigil/
│
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       └── ci.yml
│
├── app/
│   ├── services/
│   │   └── analyzer.py
│   ├── static/
│   │   ├── css/
│   │   └── img/
│   │       └── aquavigil-logo.svg
│   ├── templates/
│   ├── __init__.py
│   ├── db.py
│   ├── metrics.py
│   └── routes.py
│
├── data/
│   ├── membrane_fouling.csv
│   ├── normal_operation.csv
│   ├── quality_excursion.csv
│   ├── suricata_alerts.json
│   ├── unexpected_dosing_incident.csv
│   └── zeek_network_evidence.csv
│
├── docker/
│   ├── grafana/
│   └── prometheus.yml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ARCHITECTURE_CATALOG.md
│   ├── DEMONSTRATION_GUIDE.md
│   ├── FAILURE_RECOVERY.md
│   ├── REQUIREMENT_MATRIX.md
│   └── SECURITY.md
│
├── scripts/
├── tests/
│
├── CHANGELOG.md
├── Dockerfile
├── LICENSE
├── OPEN-AQUAVIGIL.vbs
├── README.md
├── START-AQUAVIGIL.cmd
├── STOP-AQUAVIGIL.cmd
├── docker-compose.yml
├── pytest.ini
├── requirements.txt
└── run.py
```

---

# Architecture Documentation

The README contains the primary architectural blueprints required to understand the platform without overwhelming the repository landing page.

The full architecture documentation contains **20 detailed technical views**:

|  # | Architecture View                      |
| -: | -------------------------------------- |
| 01 | Platform Context                       |
| 02 | End-to-End Evidence Architecture       |
| 03 | Logical Component Architecture         |
| 04 | Water-Quality Analysis Pipeline        |
| 05 | Desalination Intelligence Architecture |
| 06 | Asset-Health Reasoning                 |
| 07 | OT / SCADA Defensive Architecture      |
| 08 | Trust-Zone & Industrial-DMZ Model      |
| 09 | Passive Monitoring Architecture        |
| 10 | Cyber-Process Correlation              |
| 11 | Anomaly-Analysis Architecture          |
| 12 | Reporting & Audit Architecture         |
| 13 | Observability Architecture             |
| 14 | Docker Deployment Architecture         |
| 15 | Application Data Stores                |
| 16 | Safety-Boundary Architecture           |
| 17 | Failure & Recovery Architecture        |
| 18 | CI & Quality-Gate Architecture         |
| 19 | Conceptual Water-Process Context       |
| 20 | Human Decision Architecture            |

Full architecture:

[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

Architecture catalog:

[`docs/ARCHITECTURE_CATALOG.md`](docs/ARCHITECTURE_CATALOG.md)

---

# Documentation

| Document                                               | Purpose                                           |
| ------------------------------------------------------ | ------------------------------------------------- |
| [`Architecture`](docs/ARCHITECTURE.md)                 | Complete architecture and data-flow documentation |
| [`Architecture Catalog`](docs/ARCHITECTURE_CATALOG.md) | Index of architecture views                       |
| [`Demonstration Guide`](docs/DEMONSTRATION_GUIDE.md)   | Guided AquaVigil demonstration                    |
| [`Requirement Matrix`](docs/REQUIREMENT_MATRIX.md)     | Requirement-to-evidence mapping                   |
| [`Security`](docs/SECURITY.md)                         | Defensive boundaries and security considerations  |
| [`Failure & Recovery`](docs/FAILURE_RECOVERY.md)       | Troubleshooting and recovery guidance             |
| [`Changelog`](CHANGELOG.md)                            | Version history                                   |

---

# Security & Safety Boundary

> ### Defensive by Design
>
> AquaVigil is a **read-only educational defensive demonstrator**.
>
> All bundled demonstration evidence is synthetic.
>
> **AquaVigil has no industrial-control authority.**

AquaVigil is designed around:

```text
✓ Passive evidence
✓ Read-only analysis
✓ Evidence provenance
✓ Water/process reasoning
✓ Defensive OT analysis
✓ Cyber-process correlation
✓ Explainable findings
✓ Human authority
✓ Auditability
✓ Defensive monitoring
✓ Synthetic demonstrations
```

Intentionally excluded:

```text
✗ PLC manipulation
✗ SCADA write operations
✗ Pump-control commands
✗ Valve-control commands
✗ Chemical-dosing commands
✗ Process setpoint changes
✗ Safety-function manipulation
✗ Production utility credentials
✗ Real utility topology
✗ Autonomous operational response
```

**Human authority remains the final decision boundary.**

See:

[`docs/SECURITY.md`](docs/SECURITY.md)

for the complete safe-use model.

---

# Standards & Assurance Scope

AquaVigil can organize analytical context relevant to water-safety and industrial cybersecurity concepts.

Evidence-oriented mappings may relate to areas such as:

* WHO water-safety concepts;
* EPA water-quality guidance;
* applicable national water-safety requirements;
* NIST SP 800-82 industrial-control-system security guidance.

> **Framework mapping does not mean certification.**

AquaVigil does not certify regulatory compliance, laboratory validity, engineering approval, or the safety/security state of a real utility.

Real-world decisions remain the responsibility of qualified organizations and authorized personnel.

---

# Responsible AI Disclosure

AI tools assisted with portions of:

* code development;
* documentation;
* testing support;
* architecture development;
* interface development;
* original visual development.

AquaVigil is designed so that analytical behavior remains inspectable where supported.

The platform emphasizes:

```text
Deterministic Conditions
        +
Visible Analytical Methods
        +
Evidence Provenance
        +
Correlation Logic
        +
Observed Evidence
        +
Expected Conditions
        ↓
Explainable Decision Support
```

AquaVigil does **not** represent a validated production water-sector AI system.

AI-assisted analysis does not replace human authority.

---

# Demonstration Path

For an academic or technical demonstration:

1. Introduce AquaVigil and its read-only boundary.
2. Explain the evidence-processing architecture.
3. Open **Analyze Evidence**.
4. Select a bundled synthetic scenario.
5. Upload the evidence.
6. Review evidence-type detection.
7. Review SHA-256 provenance.
8. Inspect process observations.
9. Review explainable findings.
10. Open **Water Quality**.
11. Review **Desalination**.
12. Inspect **Asset Health**.
13. Open **OT / SCADA Security**.
14. Review the **Threat Center**.
15. Inspect **Zeek / Suricata** evidence.
16. Generate the professional report.
17. Review standards-related evidence.
18. Open **Prometheus**.
19. Open **Grafana**.
20. Finish with the passive-monitoring and human-authority boundaries.

---

# Limitations

AquaVigil v1.0.0 is an **educational defensive prototype**.

Its output is not:

```text
✗ Laboratory certification
✗ Engineering approval
✗ Regulatory certification
✗ Legal advice
✗ Authorization to operate infrastructure
✗ Independent water-quality verification
✗ A replacement for qualified operators
✗ A safety-system controller
```

A real-world deployment would require a separately engineered and authorized architecture including areas such as:

* authenticated access;
* identity and RBAC;
* encrypted secret management;
* hardened gateways;
* controlled evidence transfer;
* validated engineering limits;
* independent water-quality verification;
* resilient infrastructure;
* managed persistence;
* formal change control;
* site-specific risk assessment;
* cybersecurity governance;
* independent safety and security review;
* qualified operational personnel.

These capabilities are outside the v1.0.0 educational prototype.

---

# Project Status

```text
Project        AquaVigil
Version        1.0.0
Type           Educational Defensive Prototype
Architecture   Read-Only / Evidence-Driven
Deployment     Docker Compose
Application    Flask / Python
Observability  Prometheus + Grafana
License        MIT
```

---

# Contributors

### Haziq Afzal

**Co-Founder, HR Presents**

Project author focused on defensive cybersecurity, DevOps, cloud, containerization, OT/SCADA security, water-infrastructure security, and evidence-driven technology platforms.

GitHub: [@HaziqBinAfzal](https://github.com/HaziqBinAfzal)

### Ruveeha Ashfaq

**Co-Founder, HR Presents · Contributor**

Contributor to AquaVigil's development and project evolution.

GitHub: [@ruveeha33](https://github.com/ruveeha33)

---

# License

AquaVigil is released under the **MIT License**.

See [`LICENSE`](LICENSE).

---

<p align="center">
  <img src="app/static/img/aquavigil-logo.svg" alt="AquaVigil Logo" width="120">
</p>

<h2 align="center">AquaVigil</h2>

<p align="center">
  <strong>Evidence First. Water Intelligence Explained.</strong>
</p>

<p align="center">
  Defensive · Read-Only · Evidence-Driven · Explainable · Observable
</p>

<p align="center">
  <strong>Evidence → Analyze → Correlate → Explain → Human Review</strong>
</p>

<p align="center">
  <strong>v1.0.0</strong>
</p>
