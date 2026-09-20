# Failure and recovery runbook

| Failure | Observable behavior | Safe recovery |
|---|---|---|
| Unsupported or empty file | User-facing rejection; no database record | Correct the source/export and retry |
| Missing sensor values | Confidence decreases; available fields still analyzed | Validate source mapping and calibration records |
| Application restart | Web UI temporarily unavailable | `docker compose restart aquavigil`; persistent volume retains history |
| Prometheus unavailable | Application continues; monitoring link fails | Restore service and verify `up{job="aquavigil"}` |
| Grafana unavailable | Analysis continues; dashboard unavailable | Restart Grafana; provisioning recreates datasource/dashboard |
| Suspected bad deployment | Health check/regression test fails | Roll back image/tag, restore known config, rerun tests |
| High-risk evidence | Critical report and safe recommendations | Follow approved incident procedure; never treat the demo as a controller |

## Validation commands

```powershell
docker compose ps
Invoke-RestMethod http://localhost:5000/health
Invoke-WebRequest http://localhost:5000/metrics
docker compose logs --tail 100 aquavigil
```

