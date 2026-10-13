import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.process_validation import simulate_pq_batches, evaluate_pq
from src.deviation_tracking import log_deviations, check_compliance
from src.microbial_trending import simulate_microbial_series, analyze_trend


@pytest.fixture(scope="module")
def pq_df():
    return simulate_pq_batches()


def test_pq_detects_the_injected_nonconforming_batch(pq_df):
    result = evaluate_pq(pq_df)
    assert "PQ-04" in result["nonconforming_batch_ids"]


def test_pq_eventually_validates(pq_df):
    result = evaluate_pq(pq_df)
    assert result["validated"] is True


def test_deviation_logged_for_every_nonconforming_batch(pq_df):
    result = evaluate_pq(pq_df)
    deviations = log_deviations(result)
    assert len(deviations) == len(result["nonconforming_batch_ids"])


def test_compliance_check_is_genuinely_100_pct(pq_df):
    result = evaluate_pq(pq_df)
    deviations = log_deviations(result)
    compliance = check_compliance(deviations)
    assert compliance["regulatory_compliance_pct"] == 100.0


def test_microbial_trend_detects_the_injected_increase():
    df = simulate_microbial_series()
    trend = analyze_trend(df)
    assert trend["significant_upward_trend"] is True
    assert trend["slope_cfu_per_sample"] > 0


def test_microbial_trend_not_flagged_on_flat_data():
    """Confirms the trend test doesn't trivially always flag an
    increase -- a flat (zero-slope) series should not be flagged."""
    df = simulate_microbial_series(true_slope=0.0, seed=99)
    trend = analyze_trend(df)
    assert trend["significant_upward_trend"] is False
