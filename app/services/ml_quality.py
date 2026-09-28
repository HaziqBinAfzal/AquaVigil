"""Inference using the versioned, locally packaged demonstration model."""
from functools import lru_cache
from pathlib import Path

FEATURES = ("ph", "conductivity", "turbidity", "chlorine", "salinity", "temperature")


@lru_cache(maxsize=1)
def _bundle():
    import joblib
    path = Path(__file__).resolve().parents[1] / "models" / "quality-synthetic-v1.joblib"
    return joblib.load(path)  # trusted bundled artifact, never accept an uploaded model


def assess(records):
    from .analyzer import _number
    rows = []
    for index, record in enumerate(records):
        values = [_number(record, name) for name in FEATURES]
        if all(value is not None and -1e9 < value < 1e9 for value in values):
            rows.append((index, values))
    if not rows:
        return {"model": "synthetic-v1", "evaluated": 0, "flagged": 0, "note": "All six features are required."}
    bundle = _bundle()
    probabilities = bundle["model"].predict_proba([values for _, values in rows])[:, 1]
    flagged = [(rows[i][0], round(float(value), 3)) for i, value in enumerate(probabilities) if value >= .80]
    return {"model": bundle["version"], "evaluated": len(rows), "flagged": len(flagged),
            "flagged_rows": flagged[:15], "note": "Synthetic classification for investigative review, not contamination confirmation."}
