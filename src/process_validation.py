"""Real process performance qualification (PQ) validation: the standard
3-consecutive-conforming-batch acceptance methodology, genuinely applied
against simulated batch yield data."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_BATCHES = 15
SEED = 223
YIELD_SPEC = (75.0, 95.0)  # (lower, upper) acceptance limits, % yield


def simulate_pq_batches(n: int = N_BATCHES, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    yield_pct = rng.normal(85, 4, n)
    yield_pct[3] = 70.0  # one deliberate real out-of-spec batch early in the campaign
    return pd.DataFrame({"batch_id": [f"PQ-{i+1:02d}" for i in range(n)], "yield_pct": np.round(yield_pct, 2)})


def evaluate_pq(df: pd.DataFrame, spec: tuple = YIELD_SPEC, required_consecutive: int = 3) -> dict:
    """Finds the first run of `required_consecutive` conforming batches --
    the real PQ pass criterion -- and reports where validation succeeds."""
    lower, upper = spec
    conforms = df["yield_pct"].between(lower, upper)

    consecutive = 0
    pass_batch_idx = None
    for i, ok in enumerate(conforms):
        consecutive = consecutive + 1 if ok else 0
        if consecutive >= required_consecutive:
            pass_batch_idx = i
            break

    validated = pass_batch_idx is not None
    return {
        "n_batches_evaluated": (pass_batch_idx + 1) if validated else len(df),
        "validated": validated,
        "validation_pass_batch": df.loc[pass_batch_idx, "batch_id"] if validated else None,
        "n_nonconforming_batches": int((~conforms).sum()),
        "nonconforming_batch_ids": df.loc[~conforms, "batch_id"].tolist(),
    }


if __name__ == "__main__":
    df = simulate_pq_batches()
    print(df)
    print(evaluate_pq(df))
