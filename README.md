<p align="center">
  <img src="app/static/img/aquavigil-logo.svg" alt="AquaVigil Logo" width="190">
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

Instead of treating operational-process observations and cybersecurity evidence as completely separate problems, AquaVigil brings them into one evidence-driven workflow.

It can:

* validate and normalize supplied evidence;
* calculate SHA-256 provenance;
* identify supported evidence types;
* analyze water and desalination observations;
* provide asset-health context;
* analyze passive OT/SCADA security evidence;
* interpret Zeek-style and Suricata-style evidence;
* correlate cyber and process observations;
* generate explainable findings;
* preserve report and analysis history;
* expose application metrics to Prometheus;
* visualize supported telemetry through Grafana.

AquaVigil ends at **analysis, explanation, reporting, and human review**.

It does **not** control industrial infrastructure.

---

## Navigation

[Quick Start](#quick-start) ·
[Why AquaVigil](#why-aquavigil) ·
[Capabilities](#core-capabilities) ·
[Workflow](#evidence-to-decision-workflow) ·
[Architecture](#platform-architecture) ·
[Workspaces](#platform-workspaces) ·
[Example Analysis](#example-analysis-journey) ·
[Monitoring](#observability) ·
[Testing](#developer-setup--testing) ·
[Documentation](#documentation) ·
[Security](#security--safety-boundary)

---

# Why AquaVigil?

Water and desalination infrastructure combines two important realities:

**physical-process behavior** and **cybersecurity behavior**.

Looking at only one side can remove useful context.

A process observation may deserve more attention when relevant cybersecurity evidence exists at the same time. Likewise, a network alert may become more meaningful when process or asset evidence provides additional context.

AquaVigil therefore follows an **evidence-to-decision-support** model.

```mermaid
flowchart LR
    WP["💧 Water / Process Evidence"]
    CY["🛡️ Cybersecurity Evidence"]
    AS["⚙️ Asset Context"]

    WP --> COR["🔗 Cyber-Process Correlation"]
    CY --> COR
    AS --> COR

    COR --> FIND["🧠 Explainable Finding"]
    FIND --> REP["📄 Evidence-Backed Report"]
    REP --> HUMAN["👤 Human Review"]
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
| Report history               |             ✅            |
| Prometheus metrics           |             ✅            |
| Grafana visualization        |             ✅            |
| Docker Compose deployment    |             ✅            |
| Automated testing            |             ✅            |
| GitHub Actions CI            |             ✅            |
| Dependency maintenance       |             ✅            |
| Industrial-control commands  | ❌ Intentionally excluded |
| Autonomous physical response | ❌ Intentionally excluded |

---

# Evidence-to-Decision Workflow

AquaVigil follows one traceable analytical path from supplied evidence to human review.

```mermaid
flowchart LR
    A["📥 Evidence"] --> B["✓ Validate"]
    B --> C["#️⃣ SHA-256"]
    C --> D["🏷️ Classify"]
    D --> E["🔎 Analyze"]
    E --> F["🔗 Correlate"]
    F --> G["💡 Explain"]
    G --> H["📄 Report"]
    H --> I["👤 Human Review"]
```

### The important boundary

```text
Evidence
   ↓
Machine-Assisted Analysis
   ↓
Explainable Finding
   ↓
Human Review
   ↓
Independent Verification
   ↓
Authorized Decision Outside AquaVigil
```

A detection is **not** automatically converted into an operational action.

Machine-assisted analysis and operational authority remain deliberately separated.

---

# Platform Architecture

The platform is organized into distinct evidence, application, intelligence, persistence, observability, and human-review layers.

```mermaid
flowchart TB

    subgraph EVIDENCE["📥 EVIDENCE LAYER"]
        W["Water / Process"]
        D["Desalination"]
        A["Asset Evidence"]
        Z["Zeek-Style"]
        S["Suricata-Style"]
    end

    subgraph APPLICATION["⚙️ APPLICATION & ANALYSIS"]
        V["Validation"]
        P["SHA-256 Provenance"]
        T["Evidence Classification"]
        AN["Analysis Engine"]
        C["Correlation Engine"]
    end

    subgraph INTELLIGENCE["🧠 INTELLIGENCE"]
        F["Explainable Findings"]
        R["Professional Reports"]
        H["Audit / Report History"]
    end

    subgraph OBS["📊 OBSERVABILITY"]
        M["Metrics"]
        PR["Prometheus"]
        G["Grafana"]
    end

    HUMAN["👤 Human Reviewer"]

    W --> V
    D --> V
    A --> V
    Z --> V
    S --> V

    V --> P
    P --> T
    T --> AN
    AN --> C

    C --> F
    F --> R
    F --> H

    F --> M
    M --> PR
    PR --> G

    R --> HUMAN
    H --> HUMAN
```

### Architecture principle

> **Evidence enters AquaVigil. Intelligence leaves AquaVigil. Industrial commands do not.**

---

# Evidence Ingestion & Provenance

AquaVigil accepts supported structured evidence formats:

| Format | Support |
| ------ | :-----: |
| CSV    |    ✅    |
| JSON   |    ✅    |
| JSONL  |    ✅    |

The ingestion pipeline follows:

```mermaid
flowchart LR
    U["Upload"] --> V["File Validation"]
    V -->|Valid| P["Parsing"]
    V -->|Invalid| X["Safe Rejection"]
    P --> N["Normalization"]
    N --> H["SHA-256 Provenance"]
    H --> T["Evidence-Type Detection"]
    T --> A["Analysis"]
```

SHA-256 provenance helps maintain a traceable relationship between:

```text
Original Evidence
       ↓
SHA-256
       ↓
Analysis
       ↓
Findings
       ↓
Report
```

This improves reproducibility and makes it possible to identify which supplied evidence produced a particular analytical result.

Evidence is treated as **input for analysis**, not automatic proof that a real-world incident occurred.

---

# Intelligence Domains

## 💧 Water Quality

Supported evidence can include observations involving:

* pH;
* conductivity;
* turbidity;
* chlorine;
* salinity;
* temperature;
* pressure;
* flow.

AquaVigil can compare supported observations against expected analytical conditions and produce evidence-backed findings.

It does not replace laboratory verification or qualified engineering judgment.

---

## 🌊 Desalination

The desalination workspace supports reasoning involving:

* membrane indicators;
* fouling observations;
* feed/process conditions;
* specific-energy indicators;
* demand-oriented analysis;
* operational trends;
* visible decision-support reasoning.

The objective is to expose **why** an observation exists rather than displaying only a status label.

---

## ⚙️ Asset Health

Asset-related evidence provides additional context for:

* process anomalies;
* water-quality observations;
* desalination findings;
* cybersecurity correlation.

Asset-health output is evidence-based decision support and does not independently certify the physical condition of real equipment.

---

## 🛡️ OT / SCADA Security

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

## 🌐 Zeek & Suricata

### Zeek-style evidence

Example:

```text
data/zeek_network_evidence.csv
```

Can contribute:

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

Can contribute:

* IDS alerts;
* signature context;
* event metadata;
* network-security observations.

These inputs contribute to defensive analysis and correlation. They do not create active network or industrial-control capability.

---

# Cyber-Process Correlation

AquaVigil's correlation layer brings multiple evidence domains together.

```mermaid
flowchart LR

    subgraph CYBER["🛡️ CYBER CONTEXT"]
        NET["Connection Context"]
        AUTH["Authorization Context"]
        IDS["IDS / Signature Context"]
    end

    subgraph PROCESS["💧 PROCESS CONTEXT"]
        WATER["Water Evidence"]
        ASSET["Asset Context"]
        DESAL["Desalination Context"]
    end

    NET --> COR["🔗 CORRELATION ENGINE"]
    AUTH --> COR
    IDS --> COR

    WATER --> COR
    ASSET --> COR
    DESAL --> COR

    COR --> FIND["🧠 EXPLAINABLE FINDING"]

    FIND --> OBS["Observed Evidence"]
    FIND --> EXP["Expected Condition"]
    FIND --> METHOD["Detection Method"]
    FIND --> IMPACT["Potential Impact"]
    FIND --> RESPONSE["Safe Response"]
```

This allows AquaVigil to explain not only **what was observed**, but **why the observation may deserve human review**.

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

The platform therefore helps answer:

**What happened?**

**Why was it detected?**

**Which evidence supports it?**

**What should be reviewed next?**

A finding remains an analytical result.

It does not automatically prove a real-world attack, equipment failure, or water-quality incident.

---

# Platform Workspaces

| Workspace                   | Purpose                                                     |
| --------------------------- | ----------------------------------------------------------- |
| 📊 **Overview**             | High-level platform, evidence, analysis, and security state |
| 📥 **Analyze Evidence**     | Upload, validate, classify, hash, and analyze evidence      |
| 💧 **Water Quality**        | Water-quality and process observations                      |
| 🌊 **Desalination**         | Membrane, energy, demand, and process reasoning             |
| ⚙️ **Asset Health**         | Evidence-based equipment and asset context                  |
| 🛡️ **OT / SCADA Security** | Passive industrial-security analysis                        |
| 🚨 **Threat Center**        | Security findings and correlated context                    |
| 🌐 **Zeek / Suricata**      | Passive network and IDS evidence                            |
| 📄 **Reports**              | Explainable reporting and audit history                     |

---

# Example Analysis Journey

A typical demonstration might use:

```text
data/unexpected_dosing_incident.csv
```

The evidence journey becomes:

```mermaid
flowchart LR
    FILE["📄 Evidence File"]
    FILE --> VAL["✓ Validate"]
    VAL --> HASH["#️⃣ Generate Provenance"]
    HASH --> TYPE["🏷️ Detect Evidence Type"]
    TYPE --> ANALYZE["🔎 Analyze"]
    ANALYZE --> PROC["💧 Process Observation"]
    ANALYZE --> SEC["🛡️ Security Context"]
    PROC --> COR["🔗 Correlate"]
    SEC --> COR
    COR --> FIND["🧠 Explainable Finding"]
    FIND --> REPORT["📄 Report"]
    REPORT --> HUMAN["👤 Human Review"]
```

The important point is that AquaVigil does not jump from:

```text
Detection → Action
```

Instead:

```text
Detection
    ↓
Evidence
    ↓
Explanation
    ↓
Correlation
    ↓
Report
    ↓
Human Review
```

---

# OT / SCADA Safety Architecture

AquaVigil deliberately separates analysis from industrial control.

```mermaid
flowchart LR

    subgraph ENTERPRISE["Enterprise / SOC"]
        SOC["Security / Analyst"]
    end

    subgraph DMZ["Industrial DMZ"]
        GW["Controlled Gateway"]
        EXP["Exported Evidence"]
    end

    subgraph OT["OT / SCADA — Conceptual"]
        HMI["HMI"]
        SCADA["SCADA"]
        PLC["PLC / RTU"]
    end

    subgraph PHYSICAL["Physical Process — Conceptual"]
        PUMP["Pumps"]
        VALVE["Valves"]
        DOSING["Dosing"]
        TREAT["Treatment / Desalination"]
    end

    OT -->|"Passive / Exported Evidence"| EXP
    EXP --> AV["💧 AquaVigil"]
    AV --> FIND["Read-Only Findings"]
    FIND --> SOC

    SCADA --> PLC
    PLC --> PHYSICAL

    AV -. "NO CONTROL PATH" .-> BLOCK["🚫 No PLC / Pump / Valve / Dosing Commands"]
```

The OT and physical-process components shown here are conceptual context.

They do not represent a real facility topology.

---

# Observability

AquaVigil integrates **Prometheus** and **Grafana** for local observability.

```mermaid
flowchart LR
    USER["Browser"]
    APP["💧 AquaVigil<br/>:8000"]
    MET["/metrics"]
    PROM["📊 Prometheus<br/>:9090"]
    GRAF["📈 Grafana<br/>:3000"]

    USER --> APP
    APP --> MET
    MET --> PROM
    PROM --> GRAF
    USER --> GRAF
    USER --> PROM
```

Monitoring is intentionally separate from operational control.

## Default Services

| Service               | URL                             |
| --------------------- | ------------------------------- |
| 💧 AquaVigil          | `http://localhost:8000`         |
| 📊 Prometheus         | `http://localhost:9090`         |
| 🎯 Prometheus Targets | `http://localhost:9090/targets` |
| 📈 Grafana            | `http://localhost:3000`         |

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

Check container state:

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

## Docker Architecture

```mermaid
flowchart LR
    B["🌐 Browser"]

    subgraph COMPOSE["🐳 Docker Compose"]
        A["AquaVigil<br/>Container"]
        P["Prometheus<br/>Container"]
        G["Grafana<br/>Container"]
    end

    B -->|":8000"| A
    A -->|"Metrics"| P
    P -->|"Datasource"| G
    B -->|":9090"| P
    B -->|":3000"| G
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

All bundled scenarios are **synthetic** and intended for safe education, demonstration, and testing.

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

> The direct Python development route does not automatically launch Prometheus or Grafana.

---

# DevSecOps Pipeline

AquaVigil includes automated repository validation and dependency maintenance.

```mermaid
flowchart LR
    DEV["Developer Change"]
    GIT["Git Commit"]
    GH["GitHub"]
    CI["GitHub Actions"]
    TEST["Automated Tests"]
    CHECK["Validation"]
    GATE{"Quality Gate"}

    DEV --> GIT
    GIT --> GH
    GH --> CI

    CI --> TEST
    CI --> CHECK

    TEST --> GATE
    CHECK --> GATE

    GATE -->|Pass| GREEN["✅ Validated"]
    GATE -->|Fail| FIX["🔧 Fix & Re-Test"]
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

The README intentionally presents only the architecture views needed to understand AquaVigil quickly.

The full architecture documentation contains **20 detailed views**:

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

> ### 🛡️ AquaVigil is a defensive, read-only educational demonstrator.
>
> All bundled demonstration evidence is synthetic.
>
> AquaVigil has no industrial-control authority.

The system's boundary is:

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
```

## AquaVigil is designed around

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

## Intentionally excluded

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
2. Explain the evidence-to-decision workflow.
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
  <img src="app/static/img/aquavigil-logo.svg" alt="AquaVigil Logo" width="110">
</p>

<h2 align="center">💧 AquaVigil</h2>

<p align="center">
  <strong>Evidence First. Water Intelligence Explained.</strong>
</p>

<p align="center">
  Defensive · Read-Only · Evidence-Driven · Explainable · Observable
</p>

<p align="center">
  <strong>Observe → Validate → Analyze → Correlate → Explain → Report → Human Review</strong>
</p>

<p align="center">
  <strong>v1.0.0</strong>
</p>
