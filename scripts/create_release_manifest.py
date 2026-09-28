"""Create a reproducible candidate manifest; approval is a human decision."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = ["requirements.txt", "Dockerfile", "docker-compose.yml",
         "app/services/analyzer.py", "app/models/quality-synthetic-v1.joblib",
         "app/models/evaluation.json", "app/templates/dashboard.html",
         "app/templates/workspace.html", "app/templates/_monitoring_new.html",
         "app/templates/_workspace_new.html", "app/static/css/live.css"]


def main():
    manifest = {"status": "CANDIDATE — NOT APPROVED FOR OT DEPLOYMENT",
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "checks": ["pytest", "compileall", "bandit", "pip-audit", "container build"],
                "operator_approval": "REQUIRED; not recorded by this script",
                "rollback": "Use the previous reviewed image and restore the retained database volume under change control",
                "artifacts": {}}
    for relative in FILES:
        data = (ROOT / relative).read_bytes()
        manifest["artifacts"][relative] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    dest = ROOT / "release-candidate-manifest.json"
    dest.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Candidate manifest: {dest}")


if __name__ == "__main__":
    main()
