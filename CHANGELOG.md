# Changelog

## 1.0.0 - 2026-09-20

- Added a fixed-height scrollable findings panel to the Analysis page while retaining the existing Protection-only evidence panels.
- Reorganized navigation into a numbered operational journey from overview and architecture through evidence, process, protection, decisions, assurance, delivery, and monitoring.
- Expanded Architecture with defense-in-depth principles, a six-stage evidence pipeline, integrations, analytics, records, and observability components.
- Removed personal, student, and exam identifiers from application metadata and licensing text.
- Completed final typography, color, responsive-layout, provenance, and workflow polish.

## 0.5.6 - 2026-09-20

- Added true multi-domain parsing for uploaded files containing both water/process telemetry and Zeek or Suricata fields.
- Populated Water Quality and Desalination live cards from integrated uploads while retaining the same file's OT/network findings.
- Counted water and network records by their actual fields instead of forcing the complete upload into one exclusive source type.

## 0.5.5 - 2026-09-20

- Gave Water Quality and Desalination independent latest-compatible evidence state.
- Prevented later Zeek or Suricata analyses from replacing live water-quality and desalination sensor cards.
- Added visible filename and timestamp provenance above populated live sensor cards.

## 0.5.4 - 2026-09-20

- Limited fixed-height internal evidence scrolling exclusively to OT / SCADA Security and Threat Center.
- Restored normal page flow for all operations, intelligence, integration, architecture, monitoring, compliance, and DevSecOps tabs.

## 0.5.3 - 2026-09-20

- Added dedicated fixed-height scrolling evidence boxes to OT / SCADA Security and Threat Center.
- Kept protection-page headings, descriptions, metrics, and response workflow outside the scrolling evidence area.
- Added visible scroll guidance, keyboard focus support, and a cache-busted stylesheet URL.

## 0.5.2 - 2026-09-20

- Added consistent fixed-height, independently scrollable evidence boxes to every feature workspace.
- Added visible styled scrollbars and contained overscroll for alerts, findings, sensors, integrations, monitoring, architecture, compliance, optimization, and DevSecOps.
- Parallelized the four DevSecOps checks and replaced the slow external advisory request in the interactive scan with a local dependency-integrity check; the full pip-audit remains in CI.
- Kept the DevSecOps run action visible while its internal evidence panel scrolls.

## 0.5.1 - 2026-09-20

- Added one-click role-specific water-quality, membrane-fouling, Zeek, and Suricata demonstrations.
- Added explicit evidence-mismatch guidance instead of blank sensor-card areas.
- Rebuilt DevSecOps as an executable scan console with current results, explanations, timing, and raw evidence.
- Corrected Zeek and Suricata action-button contrast and separated analyze from download actions.
- Updated the one-click launcher to resolve occupied application, Prometheus, and Grafana ports automatically.

## 0.5.0 - 2026-09-20

- Added executable in-browser DevSecOps tests, compilation, Bandit, and pip-audit checks with real output.
- Added evidence-driven AI-assisted threat alerts and a live alerts API.
- Added fresh-session startup so previously stored demonstration analyses are removed when the Docker application opens.
- Added a zero-command Windows launcher that starts Docker Desktop, rebuilds the stack, waits for health, and opens the browser.
- Updated the top status indicator with the current generated-alert count.

## 0.4.0 - 2026-09-20

- Rebuilt the feature and workflow structure strictly around the six capability groups in the supplied project brief.
- Separated OT/SCADA protection from cyber-physical threat triage and public-health-first incident response.
- Expanded Zeek and Suricata into distinct explanatory, evidence-driven integration views.
- Added the required DevSecOps workflow for secure development, testing, vulnerability handling, and controlled patching.
- Added live packaged-control checks, Bandit static analysis, pip-audit dependency scanning, and Dependabot update automation.
- Redesigned Prometheus and Grafana monitoring with product-specific colors and latest-analysis values.
- Enlarged landing workflow and desalination-stage cards with clear roles and workspace links.

## 0.3.1 - 2026-09-20

- Increased desktop, navigation, card, table, and supporting-text typography for normal-resolution readability.
- Added a six-step evidence-to-action workflow and complete capability coverage to the landing page.
- Rebuilt report viewing and downloads as fully self-contained styled documents.
- Adopted the professional cover, contents, summary, score, evidence, findings, action, standards, and appendix structure used by high-quality assurance reports.
- Removed external stylesheet dependencies from downloaded HTML reports so they remain styled when opened directly from Windows.

## 0.3.0 - 2026-09-20

- Expanded evidence ingestion with automatic water/process, Zeek-style, and Suricata EVE adapters.
- Added explainable baseline detection and full observed/expected/method/impact/response details.
- Added six downloadable synthetic sample datasets.
- Rebuilt reports with professional sections, print/PDF, HTML download, and controlled deletion.
- Added an AquaVigil shield/drop logo and normalized typography across desktop and mobile layouts.
- Removed assessment-specific branding and the dedicated assessment navigation mode.
- Expanded standards mapping for WHO WSP, NIST SP 800-82 Rev. 3, IEC 62443-3-3, and EPA/AWWA practices.
- Expanded Prometheus telemetry and provisioned a 16-panel live Grafana dashboard.
- Added stored-result compatibility for reports produced by earlier versions.

## 0.2.0 - 2026-09-20

- Added the approved AquaVigil desalination hero artwork and reversed the landing-page composition.
- Replaced decorative workspace placeholders with latest-analysis sensor trends, findings, optimization values and compliance evidence.
- Added live platform status and database-backed health endpoints.
- Fixed clean-machine Docker startup by pulling Prometheus and Grafana images before launching.
- Added configurable monitoring redirection URLs and explicit manual Docker commands.

## 0.1.0 — 2026-09-19

- Initial smart-water security platform build.
- Added water/process evidence analysis and provenance.
- Added synthetic unauthorized-dosing incident correlation.
- Added constrained optimization indicators and printable reports.
- Added Prometheus/Grafana observability, tests and demonstration documentation.
- Added Windows and macOS/Linux one-click Docker launchers with engine checks, configurable ports, readiness polling and browser opening.
- Hero image remains at the required approval checkpoint.
