# 15–20 minute platform demonstration

## Start the complete stack

From PowerShell in the project folder:

```powershell
Copy-Item .env.example .env -ErrorAction SilentlyContinue
docker compose pull prometheus grafana
docker compose up --build -d
docker compose ps
```

Open `http://localhost:8000`. Use `docker compose down` after the demonstration.

## 0:00–2:00 — purpose and safety boundary

State the objective: protect public health while preserving secure, resilient and efficient water production. Explain that AquaVigil analyzes exported synthetic evidence and cannot control a plant.

## 2:00–5:00 — architecture defense

Open **Architecture**. Explain the five trust zones from treatment upward. Emphasize the industrial DMZ, approved flows, passive visibility, independent quality verification and absence of a direct enterprise-to-controller path.

## 5:00–9:00 — end-to-end incident

Open **Analyze Evidence**, choose the supplied dosing scenario, and show:

1. File provenance and SHA-256.
2. Sensor validation across pH, conductivity, turbidity, chlorine, salinity, pressure, flow and temperature.
3. Unexpected dosing command correlated with authorization and process change.
4. Risk classification based on cyber and public-health consequence.
5. Safe recommendation: contain command path, independently verify quality, restore validated configuration and preserve evidence.

## 9:00–12:00 — AI and optimization

Explain that the fouling and energy indicators are transparent demonstration heuristics. They support a supervised inspection decision. They do not override engineering envelopes, water-quality limits or the operator.

## 12:00–15:00 — reporting and compliance

Open the HTML report. Show source hash, detection details, recommendations and WHO/EPA/NIST evidence mappings. Say clearly: “This is a demonstration mapping, not formal certification.”

## 15:00–18:00 — monitoring, failure and recovery

Open Prometheus and Grafana. Show analysis, risk and findings metrics. Upload an unsupported file to demonstrate safe rejection. Explain that the persistent SQLite volume survives an application restart.

## Q&A defenses

- **Why passive monitoring?** It provides visibility without injecting commands into fragile OT systems.
- **Why an industrial DMZ beyond a firewall?** It provides controlled services—jump access, historian replication, patch staging and file transfer—without direct enterprise/OT sessions.
- **Why validate sensors before ML?** A faulty or uncalibrated sensor can create a false contamination alarm and unsafe response.
- **Why not automate containment?** Public-health and process consequences require approved procedures and qualified operator authority.
- **What scales first?** Database, evidence storage, background processing, authentication and redundant deployment.
- **Key trade-off?** Faster detection versus false positives; confidence comes from corroboration and independent verification.
