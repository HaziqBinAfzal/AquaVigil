"""Exploratory models for ordered process evidence."""

def next_flow_projection(values):
    if len(values) < 12:
        return {"available": False, "reason": "At least 12 ordered flow readings are required."}
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.metrics import mean_absolute_error

    series = np.asarray(values, dtype=float)
    train_end = max(8, int(len(series) * .75))
    x = np.arange(len(series), dtype=float).reshape(-1, 1)
    model = Ridge(alpha=10.0).fit(x[:train_end], series[:train_end])
    error = mean_absolute_error(series[train_end:], model.predict(x[train_end:]))
    model.fit(x, series)
    projection = max(0.0, float(model.predict([[len(series)]])[0]))
    return {"available": True, "projected_next_flow_m3_h": round(projection, 2),
            "holdout_mae_m3_h": round(float(error), 2),
            "training_records": train_end, "holdout_records": len(series) - train_end,
            "assumptions": "Record order represents time; next-record projection only. Validate intervals and plant data before use."}

def screen_pressure_flow(records):
    """Fit earlier pressure/flow pairs and screen later observations."""
    if len(records) < 24:
        return {"available": False, "reason": "At least 24 ordered records with both pressure and flow are required."}

    from sklearn.ensemble import IsolationForest

    baseline_count = len(records) * 3 // 4
    baseline = [values for _, values in records[:baseline_count]]
    if all(values == baseline[0] for values in baseline):
        return {"available": False, "reason": "Earlier pressure and flow records must contain some variation."}
    later = records[baseline_count:]
    model = IsolationForest(n_estimators=100, contamination=0.10, random_state=133)
    model.fit(baseline)
    scores = model.decision_function([values for _, values in later])
    flagged = [
        {"record": index, "pressure_bar": pressure, "flow_m3_h": flow,
         "score": round(float(score), 4)}
        for (index, (pressure, flow)), score in zip(later, scores)
        if score < 0
    ]
    return {"available": True, "baseline_records": baseline_count,
            "screened_records": len(later), "flagged_count": len(flagged),
            "flagged_records": flagged[:10]}
