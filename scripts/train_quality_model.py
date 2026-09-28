"""Build a transparent demonstration classifier from generated, labeled samples.

These examples are synthetic and must never be interpreted as calibrated plant data.
"""
import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ["ph", "conductivity", "turbidity", "chlorine", "salinity", "temperature"]


def generate(seed=133, count=1200):
    rng = np.random.default_rng(seed)
    x = rng.normal([7.15, 650, .32, 1.1, .22, 24],
                   [.23, 155, .12, .26, .055, 1.8], size=(count, len(FEATURES)))
    y = np.zeros(count, dtype=int)
    # Inject an independent excursion into half the rows, then shuffle.
    for row in range(count // 2, count):
        feature = row % 5
        x[row, feature] = ([5.8, 1900, 2.1, .05, .72][feature])
        y[row] = 1
    indices = rng.permutation(count)
    return x[indices], y[indices]


def main():
    x, y = generate()
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=.25, random_state=133, stratify=y)
    model = RandomForestClassifier(n_estimators=90, max_depth=7, min_samples_leaf=3, random_state=133)
    model.fit(train_x, train_y)
    predicted = model.predict(test_x)
    metrics = classification_report(test_y, predicted, output_dict=True, zero_division=0)
    dest = ROOT / "app" / "models"
    dest.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "version": "synthetic-v1"}, dest / "quality-synthetic-v1.joblib")
    (dest / "evaluation.json").write_text(json.dumps({
        "dataset": "generated synthetic samples, seed 133; no field calibration",
        "features": FEATURES, "training_samples": int(len(train_x)), "holdout_samples": int(len(test_x)),
        "confusion_matrix": confusion_matrix(test_y, predicted).tolist(),
        "holdout_precision": round(metrics["1"]["precision"], 3),
        "holdout_recall": round(metrics["1"]["recall"], 3),
        "holdout_f1": round(metrics["1"]["f1-score"], 3),
        "limitations": "Generated normal and injected excursion patterns; not validated for contamination or actual plant conditions."
    }, indent=2))
    print("Synthetic quality model and holdout evaluation saved in app/models.")


if __name__ == "__main__":
    main()
