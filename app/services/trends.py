"""Short-horizon exploratory trend fit with chronological holdout."""
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
    projection = max(0.0, float(model.predict([[len(series)]])[0]))
    return {"available": True, "projected_next_flow_m3_h": round(projection, 2),
            "holdout_mae_m3_h": round(float(error), 2),
            "training_records": train_end, "holdout_records": len(series) - train_end,
            "assumptions": "Record order represents time; next-record projection only. Validate intervals and plant data before use."}
