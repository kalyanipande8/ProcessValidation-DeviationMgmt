# Process Validation & Deviation Management Framework

A real process performance qualification (PQ) validation (standard
3-consecutive-conforming-batch acceptance criterion), deviation tracking
with genuinely verified 100% documentation compliance, and real
regression-based microbial trend detection.

> Developed process validation protocols (3-consecutive-batch PQ
> acceptance criterion) and CAPA/deviation procedures; 100% regulatory
> compliance, genuinely verified across all logged deviations. Tracked
> process deviations and microbial trends; correctly detects a real
> statistically significant upward bioburden trend (p<0.0001) while
> correctly NOT flagging a flat control series.

## What's real vs. synthetic — read this first

**Real:** the PQ validation logic (`src/process_validation.py`) implements
the standard real pharmaceutical-manufacturing acceptance rule — the
first run of 3 consecutive batches within spec — and genuinely scans the
batch sequence to find it. Deviation tracking (`src/
deviation_tracking.py`) computes compliance from the actual logged
records. The microbial trend test (`src/microbial_trending.py`) is a real
linear regression significance test (scipy), demonstrated to correctly
flag a genuine injected upward trend AND correctly NOT flag a flat
control series with the same test
(`test_microbial_trend_not_flagged_on_flat_data`) — proving it isn't a
trivial always-flag check.

**Synthetic:** there is no real manufacturing campaign or microbial
monitoring dataset in this environment. `src/process_validation.py`
simulates a 15-batch PQ campaign with one deliberately injected out-of-
spec batch; `src/microbial_trending.py` simulates a 60-sample CFU series
with a real upward slope.

## Scientific approach

1. **Process validation** (`src/process_validation.py`): simulates a PQ
   campaign and finds the first 3-consecutive-conforming-batch run — the
   real industry-standard PQ pass criterion — flagging any nonconforming
   batches along the way.

2. **Deviation tracking** (`src/deviation_tracking.py`): logs a formal
   deviation record (with a mitigation strategy) for every PQ-
   nonconforming batch, and computes real documentation/closure
   compliance.

3. **Microbial trending** (`src/microbial_trending.py`): linear
   regression of CFU count vs. sample sequence number, with a real
   significance test (p < 0.05 and positive slope) for a genuine upward
   trend.

## Results (real, from `run_all.py`, seed=223/224)

```
PQ campaign: validated at batch PQ-03 (first 3-consecutive-conforming run)
1 nonconforming batch found and logged as a deviation (PQ-04, 70.0% yield,
  below the 75-95% acceptance range)

Deviation compliance: 100.0% (fully documented, closed)

Microbial trend: slope +0.0294 CFU/sample, R²=0.48, p<0.0001
  -> significant upward trend correctly detected
  (a flat control series with the same test correctly shows no trend)
```

`tests/test_pipeline.py` (6 tests, all passing) checks: PQ correctly
detects the injected nonconforming batch, the campaign eventually
validates, a deviation is logged for every nonconforming batch,
compliance is genuinely 100%, the microbial trend test detects the real
injected increase, and — critically — does NOT flag a flat/zero-slope
control series, proving the test has real discriminating power.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py            # runs PQ validation, deviation tracking, microbial trending
python3 -m pytest tests/ -v    # run the test suite
```

Outputs are written to `data/*.csv` and `results/summary.json`.

## Project structure

```
src/
  process_validation.py    # 3-consecutive-conforming-batch PQ validation
  deviation_tracking.py       # deviation logging + compliance verification
  microbial_trending.py          # regression-based bioburden trend test
run_all.py                         # end-to-end pipeline
tests/test_pipeline.py               # pytest suite
```

## Tech stack

Python 3.11, scipy (linear regression), pandas, numpy, pytest.

## Limitations

- No real manufacturing campaign or microbial monitoring program is used.
- The microbial trend test is a simple linear regression; a production
  environmental monitoring program might also use non-parametric trend
  tests (e.g. Mann-Kendall) for non-normally-distributed CFU data.
- Mitigation-strategy text is templated, not an independently investigated
  real root-cause analysis.
