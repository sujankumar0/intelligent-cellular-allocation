import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_predictor(seed=42):
    """Train a demo model on synthetic historical traffic features."""
    rng = np.random.default_rng(seed)
    n = 1800
    hour = rng.integers(0, 24, n)
    previous = rng.uniform(5, 130, n)
    recent_avg = np.clip(previous + rng.normal(0, 12, n), 1, 140)
    day_factor = rng.uniform(0.75, 1.25, n)
    rush = np.where(((hour >= 7) & (hour <= 10)) | ((hour >= 17) & (hour <= 21)), 12, -3)
    target = np.clip(0.58 * previous + 0.42 * recent_avg + rush, 1, 140) * day_factor
    target += rng.normal(0, 5, n)
    X = np.column_stack([hour, previous, recent_avg, day_factor])
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=seed, n_jobs=-1)
    model.fit(X, target)
    return model

def predict_demands(loads, seed=42):
    model = train_predictor(seed)
    # A reproducible hour-of-day feature; recent average is approximated from current load.
    predictions = {}
    for idx, (cell, users) in enumerate(loads.items()):
        hour = 8 if idx % 2 == 0 else 19
        recent_avg = max(1, users * (0.94 + 0.04 * (idx % 3)))
        features = np.array([[hour, users, recent_avg, 1.0]])
        predictions[cell] = float(np.clip(model.predict(features)[0], 1, 140))
    return predictions
