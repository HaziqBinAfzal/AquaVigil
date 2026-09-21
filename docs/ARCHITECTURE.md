# AquaVigil Architecture

> **Scope:** AquaVigil is a defensive, read-only educational prototype. The diagrams below describe the software demonstration and conceptual trust boundaries. They do not authorize connection to, or control of, real water utilities, SCADA systems, PLCs, pumps, valves, dosing systems, or safety functions.

## 1. Platform context

```mermaid
flowchart LR
    U[Analyst / Student] --> UI[AquaVigil Web Interface]
    UI --> ING[Evidence Ingestion]
    ING --> ANA[Analysis & Correlation]
    ANA --> FIND[Explainable Findings]
    FIND --> REP[Reports & Audit History]
    UI --> MET[Prometheus Metrics]
    MET --> GRA[Grafana Dashboard]
    SYN[Synthetic / Exported Evidence] --> ING
    SAFE[Read-Only Safety Boundary] --- UI
```

AquaVigil accepts exported evidence, validates it, analyzes water/process and cybersecurity observations, correlates findings, and presents traceable results. It does not send operational commands.

## 2. End-to-end evidence architecture

```mermaid
flowchart LR
    A[CSV] --> V[Validation]
    B[JSON] --> V
    C[JSONL] --> V
    V -->|Invalid| X[Safe Rejection]
    V -->|Valid| H[SHA-256 Provenance]
    H --> T[Evidence-Type Detection]
    T --> W[Water / Process Pipeline]
    T --> O[OT / SCADA Pipeline]
    T --> Z[Zeek / Suricata Pipeline]
    W --> C1[Correlation]
    O --> C1
    Z --> C1
    C1 --> E[Explainable Findings]
    E --> D[(SQLite Audit Store)]
    E --> R[Professional Report]
    E --> M[Metrics]
```

## 3. Logical component architecture

```mermaid
flowchart TB
    subgraph PRESENTATION["Presentation Layer"]
        HOME[Overview]
        UP[Analyze Evidence]
        WQ[Water Quality]
        DES[Desalination]
        AH[Asset Health]
        SEC[OT / SCADA Security]
        TC[Threat Center]
        INT[Zeek / Suricata]
        REPORTS[Reports]
    end

    subgraph APP["Application Layer"]
        ROUTES[Flask Routes]
        ANALYZER[Analysis Service]
        METRICS[Metrics Service]
        DBL[Database Service]
    end

    subgraph DATA["Data Layer"]
        FILES[Synthetic Evidence Files]
        DB[(SQLite)]
    end

    subgraph OBS["Observability"]
        PROM[Prometheus]
        GRAF[Grafana]
    end

    PRESENTATION --> ROUTES
    ROUTES --> ANALYZER
    ROUTES --> DBL
    ROUTES --> METRICS
    ANALYZER --> FILES
    DBL --> DB
    METRICS --> PROM
    PROM --> GRAF
```

## 4. Water-quality analysis pipeline

```mermaid
flowchart LR
    E[Water Evidence] --> P[Parse & Normalize]
    P --> Q[Quality Parameter Checks]
    Q --> PH[pH]
    Q --> TU[Turbidity]
    Q --> CL[Chlorine]
    Q --> CO[Conductivity]
    Q --> SA[Salinity]
    Q --> TE[Temperature]
    PH --> F[Findings]
    TU --> F
    CL --> F
    CO --> F
    SA --> F
    TE --> F
    F --> EX[Observed / Expected / Method / Impact / Response]
```

## 5. Desalination intelligence architecture

```mermaid
flowchart LR
    FEED[Feed / Process Evidence] --> N[Normalize]
    N --> MEM[Membrane Indicators]
    N --> EN[Specific Energy Indicators]
    N --> DEM[Demand Indicators]
    MEM --> DS[Desalination Decision Support]
    EN --> DS
    DEM --> DS
    DS --> WHY[Visible Reasoning]
    WHY --> REP[Report]
```

## 6. Asset-health reasoning

```mermaid
flowchart LR
    P[Pressure] --> A[Asset Context]
    F[Flow] --> A
    T[Temperature] --> A
    Q[Quality Observations] --> A
    A --> B[Baseline / Range Checks]
    B --> H[Health Finding]
    H --> C[Context & Safe Response]
```

## 7. OT / SCADA defensive architecture

```mermaid
flowchart TB
    subgraph ENTERPRISE["Enterprise / SOC"]
        SOC[Security Operations]
    end

    subgraph DMZ["Industrial DMZ"]
        GW[Controlled Gateway]
        EXP[Exported Evidence]
    end

    subgraph OT["OT / SCADA Zone - Conceptual"]
        HMI[HMI]
        SCADA[SCADA]
        PLC[PLC / RTU]
    end

    subgraph PROCESS["Water Process - Conceptual"]
        PUMP[Pumps]
        VALVE[Valves]
        DOSING[Dosing]
        TREAT[Treatment / Desalination]
    end

    SOC -->|Approved flow| GW
    OT -->|Passive / exported evidence| EXP
    EXP --> AV[AquaVigil]
    AV --> FIND[Read-Only Findings]
    SCADA --> PLC
    PLC --> PROCESS

    AV -. No control path .-> X[No PLC / Pump / Valve Commands]
```

## 8. Trust-zone and industrial-DMZ model

```mermaid
flowchart LR
    E[Enterprise Zone] -->|Approved / filtered| D[Industrial DMZ]
    D -->|Controlled gateway| O[OT / SCADA Zone]
    O --> S[Safety & Quality Functions]
    S --> P[Water / Desalination Process]
    O -->|Exported passive evidence| AV[AquaVigil]
    AV --> SOC[Analyst / SOC Review]
```

There is deliberately no direct AquaVigil-to-process command path.

## 9. Passive monitoring architecture

```mermaid
flowchart LR
    NET[Exported Network Evidence] --> Z[Zeek-Style Connections]
    IDS[Exported IDS Evidence] --> S[Suricata EVE-Style Events]
    Z --> N[Network Context]
    S --> A[Alert Context]
    N --> C[Security Correlation]
    A --> C
    PROC[Process Evidence] --> C
    C --> T[Threat Center]
    C --> R[Explainable Report]
```

## 10. Cyber-process correlation

```mermaid
flowchart TB
    C1[Connection / Zone Context] --> COR[Correlation Engine]
    C2[Authorization Context] --> COR
    C3[Signature / IDS Context] --> COR
    C4[Water / Process Context] --> COR
    C5[Asset Context] --> COR
    COR --> P[Prioritized Finding]
    P --> E1[Evidence]
    P --> E2[Expected Condition]
    P --> E3[Method]
    P --> E4[Impact]
    P --> E5[Safe Response]
```

## 11. Anomaly-analysis architecture

```mermaid
flowchart LR
    E[Recent Evidence] --> B[Transparent Recent Baseline]
    E --> R[Deterministic Range Checks]
    B --> A[Deviation Assessment]
    R --> A
    A --> F[Anomaly Finding]
    F --> H[Human Review]
```

AquaVigil's anomaly layer is decision support, not autonomous process control.

## 12. Reporting and audit architecture

```mermaid
flowchart LR
    F[Explainable Findings] --> R[Report Builder]
    P[SHA-256 Provenance] --> R
    S[Standards Evidence Mapping] --> R
    R --> H[HTML Report]
    H --> PDF[Print / PDF Workflow]
    R --> DB[(Report / Audit History)]
    DB --> HIST[History View]
    HIST --> DEL[Controlled Deletion]
```

## 13. Observability architecture

```mermaid
flowchart LR
    APP[AquaVigil Application] -->|Metrics endpoint| PROM[Prometheus]
    PROM --> GRAF[Grafana]
    GRAF --> DASH[Water Operations Dashboard]
    PROM --> HEALTH[Service / Analysis Telemetry]
    APP -. No operational control .-> SAFE[Read-Only Boundary]
```

## 14. Docker deployment architecture

```mermaid
flowchart TB
    HOST[Local Computer]
    BROWSER[Browser]

    subgraph COMPOSE["Docker Compose"]
        APP[AquaVigil Container]
        PROM[Prometheus Container]
        GRAF[Grafana Container]
    end

    BROWSER -->|HTTP 8000| APP
    APP -->|Metrics| PROM
    PROM -->|Datasource| GRAF
    BROWSER -->|HTTP 3000| GRAF
    BROWSER -->|HTTP 9090| PROM
    HOST --> COMPOSE
```

## 15. Application data stores

```mermaid
flowchart LR
    UP[Uploaded / Bundled Evidence] --> MEM[Read-Only Parsing]
    MEM --> HASH[SHA-256]
    MEM --> ANA[Analysis]
    ANA --> DB[(SQLite Audit Store)]
    ANA --> REP[Generated Report]
    ANA --> MET[Prometheus Metrics]
```

## 16. Safety-boundary architecture

```mermaid
flowchart TB
    REAL[Real Utility / Real SCADA / Real Controllers]
    SEP[Explicit Separation Boundary]
    SYN[Synthetic or Exported Evidence]
    AV[AquaVigil]
    HUMAN[Human Reviewer]

    REAL -. Not directly connected .-> SEP
    SEP --> SYN
    SYN --> AV
    AV --> HUMAN
    AV -. No commands .-> BLOCK[No Pump / Valve / PLC / Dosing Control]
```

## 17. Failure and recovery architecture

```mermaid
flowchart LR
    START[Launcher] --> D{Docker Available?}
    D -->|No| ERR[Visible Diagnostic]
    D -->|Yes| C[Docker Compose]
    C --> H{AquaVigil Healthy?}
    H -->|No| LOG[Container / Launcher Diagnostics]
    H -->|Yes| READY[Application Ready]
    LOG --> FIX[Recover Port / Engine / Configuration]
    FIX --> C
    READY --> STOP[Controlled Shutdown]
```

## 18. CI and quality-gate architecture

```mermaid
flowchart LR
    DEV[Repository Change] --> GH[GitHub]
    GH --> CI[GitHub Actions]
    CI --> TEST[Automated Tests]
    CI --> DEP[Dependency / Configuration Checks]
    TEST --> PASS{Pass?}
    DEP --> PASS
    PASS -->|Yes| GREEN[Quality Gate Pass]
    PASS -->|No| FIX[Fix Before Release]
```

## 19. Conceptual water-process context

```mermaid
flowchart LR
    SOURCE[Source / Intake] --> PRE[Pre-Treatment]
    PRE --> DESAL[Desalination / Treatment]
    DESAL --> POST[Post-Treatment / Quality]
    POST --> STORE[Storage]
    STORE --> DIST[Distribution]

    SENSOR[Exported Sensor Evidence] -. Observations .-> PRE
    SENSOR -. Observations .-> DESAL
    SENSOR -. Observations .-> POST
    SENSOR -. Observations .-> DIST
    SENSOR --> AV[AquaVigil Analysis]
```

This diagram is conceptual and does not represent a real facility topology.

## 20. Human decision architecture

```mermaid
flowchart LR
    E[Evidence] --> A[AquaVigil Analysis]
    A --> F[Explainable Finding]
    F --> H[Human Review]
    H --> V[Independent Verification]
    V --> D[Authorized Operational Decision Outside AquaVigil]
```

AquaVigil ends at evidence-backed decision support. Operational authority remains outside the application.

## Architecture principles

1. **Read-only by design.** AquaVigil analyzes and visualizes; it does not operate infrastructure.
2. **Evidence before claims.** Findings originate from supplied evidence and retain provenance.
3. **Explainability.** Findings expose the observed condition, expected condition, method, impact, source, and safe response.
4. **Separation of concerns.** Presentation, analysis, persistence, and observability remain distinct.
5. **Passive security context.** Zeek/Suricata-style evidence is consumed as exported evidence rather than captured through an active control path.
6. **Human authority.** Findings support review; they do not replace qualified operators, laboratory verification, or engineering approval.
7. **Reproducible deployment.** Docker Compose defines the application, Prometheus, and Grafana stack.
8. **Safe demonstration.** Bundled datasets are synthetic and suitable for educational testing.

## Current implementation mapping

| Architecture area | Repository implementation |
|---|---|
| Web application | `app/` |
| Routes and workspace views | `app/routes.py`, `app/templates/` |
| Analysis engine | `app/services/analyzer.py` |
| Persistence | `app/db.py` |
| Metrics | `app/metrics.py` |
| Synthetic evidence | `data/` |
| Prometheus | `docker/prometheus.yml` |
| Grafana | `docker/grafana/` |
| Container stack | `docker-compose.yml` |
| Tests | `tests/` |
| Launchers | `OPEN-AQUAVIGIL.vbs`, `START-AQUAVIGIL.cmd`, `start-aquavigil.ps1`, `start-aquavigil.sh` |

## Deployment note

The current v1.0.0 Docker Compose model intentionally stays small: AquaVigil, Prometheus, and Grafana. A production utility architecture would require a separately engineered and authorized design including identity, RBAC, encrypted secret management, hardened gateways, controlled evidence transfer, redundant services, managed persistence, signed reports, formal change control, and independent safety/security review. Those capabilities are outside the v1.0.0 educational prototype.
