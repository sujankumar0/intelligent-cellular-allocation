import numpy as np
import pandas as pd

CELLS = [f"BS{i}" for i in range(1, 7)]

def generate_traffic(mode="Mixed", seed=42, n_rounds=24):
    """Generate reproducible synthetic user-demand observations."""
    rng = np.random.default_rng(seed)
    rows = []
    base_profiles = {
        "Low":    [18, 22, 15, 20, 17, 19],
        "Medium": [48, 55, 42, 58, 46, 52],
        "High":   [92, 105, 85, 110, 96, 101],
        "Mixed":  [25, 48, 75, 35, 90, 55],
        "Sudden spike": [25, 30, 28, 32, 26, 29],
    }
    base = np.array(base_profiles[mode], dtype=float)
    for t in range(n_rounds):
        values = base + rng.normal(0, max(3, base.mean() * 0.10), size=6)
        if mode == "Sudden spike" and t >= n_rounds // 2:
            values[0] += 65
            values[3] += 35
        values = np.clip(values, 1, 140).round().astype(int)
        for cell, users in zip(CELLS, values):
            rows.append({"round": t + 1, "base_station": cell, "active_users": int(users)})
    return pd.DataFrame(rows)

def current_loads(mode="Mixed", seed=42, n_rounds=24):
    data = generate_traffic(mode, seed, n_rounds)
    latest = data[data["round"] == data["round"].max()]
    return dict(zip(latest["base_station"], latest["active_users"]))
