"""End-to-end: run PQ process validation, log and verify compliance for
any deviations, and test the microbial trend for a significant increase."""
import json
import os

from src.process_validation import simulate_pq_batches, evaluate_pq
from src.deviation_tracking import log_deviations, check_compliance
from src.microbial_trending import simulate_microbial_series, analyze_trend

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

print("=== Process validation (PQ campaign, 3-consecutive-conforming-batch criterion) ===")
pq_df = simulate_pq_batches()
pq_df.to_csv("data/pq_batches.csv", index=False)
print(pq_df)
pq_result = evaluate_pq(pq_df)
print(pq_result)

print("\n=== Deviation tracking ===")
deviations = log_deviations(pq_result)
deviations.to_csv("data/deviations.csv", index=False)
print(deviations)

print("\n=== Regulatory compliance check ===")
compliance = check_compliance(deviations)
print(compliance)

print("\n=== Microbial (bioburden) trend analysis ===")
microbial_df = simulate_microbial_series()
microbial_df.to_csv("data/microbial_series.csv", index=False)
trend = analyze_trend(microbial_df)
print(trend)

summary = {
    "pq_validated": pq_result["validated"],
    "pq_validation_pass_batch": pq_result["validation_pass_batch"],
    "n_deviations_logged": len(deviations),
    "regulatory_compliance_pct": compliance["regulatory_compliance_pct"],
    "microbial_trend_slope": trend["slope_cfu_per_sample"],
    "microbial_trend_p_value": trend["p_value"],
    "significant_upward_microbial_trend": trend["significant_upward_trend"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
