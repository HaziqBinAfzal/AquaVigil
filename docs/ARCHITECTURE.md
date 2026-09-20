# AquaVigil architecture

## System architecture

```mermaid
flowchart TB
  U[Student / operator] --> W[Flask web application]
  W --> V[Validation and provenance]
  V --> A[Quality, OT and optimization analysis]
  A --> D[(SQLite audit store)]
  A --> R[HTML assurance report]
  W --> M[Prometheus metrics]
  M --> G[Grafana dashboard]
```

## Water infrastructure trust zones

```mermaid
flowchart TB
  E[Enterprise and SOC] -->|approved flows| I[Industrial DMZ]
  I -->|controlled gateway| O[OT and SCADA]
  O -->|process evidence| S[Safety and quality]
  S -->|independent verification| T[Treatment process]
```

There is deliberately no direct enterprise-to-treatment command path. The demonstration application consumes exported synthetic evidence; it does not connect to these zones.

## Data-flow diagram

```mermaid
flowchart LR
  F[CSV or JSON] --> C{Validate}
  C -->|invalid| X[Safe rejection]
  C -->|valid| H[SHA-256 provenance]
  H --> Q[Sensor validation]
  Q --> K[Cyber-process correlation]
  K --> P[Prioritized findings]
  P --> DB[(Audit history)]
  P --> RP[HTML report]
```

## Security architecture

| Boundary | Control | Rationale |
|---|---|---|
| Browser → application | File type/size checks and safe parsing | Reduces malformed input and resource risk |
| Evidence → analysis | In-memory read-only parsing and SHA-256 hash | Preserves provenance without altering the source |
| Application → database | Parameterized SQLite queries | Prevents SQL injection in stored fields |
| Application → monitoring | Metrics-only endpoint | Observability without operational control |
| Report → reviewer | Explicit limitations and evidence references | Prevents overstated conclusions |

## Deployment model

The Docker Compose stack is intentionally small enough for one student to explain: one application, one Prometheus service and one Grafana service. For enterprise scale, replace SQLite with managed PostgreSQL, use object storage for evidence, add authentication/RBAC, queue long-running analysis, sign reports, encrypt secrets and deploy redundant stateless application replicas behind a reverse proxy.
