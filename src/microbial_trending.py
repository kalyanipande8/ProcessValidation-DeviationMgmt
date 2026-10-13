"""Real microbial (bioburden) trend analysis: linear regression of CFU
counts over batch sequence, with a significance test for a genuine
upward trend -- the standard trending methodology for environmental/
bioburden monitoring programs."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

N_SAMPLES = 60
SEED = 224


def simulate_microbial_series(n: int = N_SAMPLES, seed: int = SEED, true_slope: float = 0.03) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    time_idx = np.arange(n)
    cfu = 1.0 + true_slope * time_idx + rng.normal(0, 0.6, n)
    cfu = np.clip(cfu, 0, None)
    return pd.DataFrame({"sample_number": time_idx, "cfu_per_100ml": np.round(cfu, 2)})


def analyze_trend(df: pd.DataFrame, alpha: float = 0.05) -> dict:
    slope, intercept, r, p_value, se = stats.linregress(df["sample_number"], df["cfu_per_100ml"])
    return {
        "slope_cfu_per_sample": round(float(slope), 5), "r_squared": round(float(r ** 2), 4),
        "p_value": round(float(p_value), 6), "significant_upward_trend": bool(p_value < alpha and slope > 0),
    }


if __name__ == "__main__":
    df = simulate_microbial_series()
    print(analyze_trend(df))
