"""Analyze synthetic research outcomes.

This public example uses synthetic data only.
It demonstrates how observed, unresolved, and censored outcomes
can be kept separate instead of treating missing observations as 0% returns.
"""

import csv
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import mean, median


SAMPLE = (
    Path(__file__).resolve().parents[1]
    / "samples"
    / "synthetic_outcomes.csv"
)

REQUIRED_FIELDS = {
    "signal_id",
    "symbol",
    "session",
    "observed_at",
    "horizon_min",
    "target_at",
    "actual_observed_at",
    "reference_price",
    "outcome_price",
    "status",
}

VALID_STATUSES = {"OBSERVED", "UNRESOLVED", "CENSORED"}


def positive_decimal(value):
    """Return a finite positive Decimal or None."""
    if value is None:
        return None

    try:
        number = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        return None

    if not number.is_finite() or number <= 0:
        return None

    return number


def price_change_pct(reference_price, outcome_price):
    """Calculate percentage price change."""
    return (outcome_price / reference_price - 1) * 100


def analyze(rows):
    counts = Counter(
        total=0,
        observed=0,
        unresolved=0,
        censored=0,
        duplicate=0,
        invalid=0,
    )

    seen = set()
    horizon_returns = defaultdict(list)
    horizon_status = defaultdict(Counter)

    for row in rows:
        counts["total"] += 1

        signal_id = (row.get("signal_id") or "").strip()
        horizon_text = (row.get("horizon_min") or "").strip()
        status = (row.get("status") or "").strip().upper()

        if not signal_id or not horizon_text:
            counts["invalid"] += 1
            continue

        try:
            horizon = int(horizon_text)
        except ValueError:
            counts["invalid"] += 1
            continue

        if horizon <= 0 or status not in VALID_STATUSES:
            counts["invalid"] += 1
            continue

        key = (signal_id, horizon)

        if key in seen:
            counts["duplicate"] += 1
            continue

        seen.add(key)
        
        if status == "UNRESOLVED":
            counts["unresolved"] += 1
            horizon_status[horizon]["UNRESOLVED"] += 1
            continue
        
        if status == "CENSORED":
            counts["censored"] += 1
            horizon_status[horizon]["CENSORED"] += 1
            continue
        
        reference_price = positive_decimal(row.get("reference_price"))
        outcome_price = positive_decimal(row.get("outcome_price"))
        actual_observed_at = (row.get("actual_observed_at") or "").strip()
        
        if (
            reference_price is None
            or outcome_price is None
            or not actual_observed_at
        ):
            counts["invalid"] += 1
            continue
        
        change = price_change_pct(reference_price, outcome_price)
        
        counts["observed"] += 1
        horizon_status[horizon]["OBSERVED"] += 1
        horizon_returns[horizon].append(change)
        
    return counts, horizon_returns, horizon_status


def print_summary(counts, horizon_returns, horizon_status):
    print("SYNTHETIC RESEARCH OUTCOME DEMO - not real market results")
    print()

    print("STATUS SUMMARY")
    print(f"total: {counts['total']}")
    print(f"observed: {counts['observed']}")
    print(f"unresolved: {counts['unresolved']}")
    print(f"censored: {counts['censored']}")
    print(f"duplicate: {counts['duplicate']}")
    print(f"invalid: {counts['invalid']}")

    print()
    print("HORIZON SUMMARY")

    horizons = sorted(
        set(horizon_status.keys()) | set(horizon_returns.keys())
    )

    for horizon in horizons:
        statuses = horizon_status[horizon]
        returns = horizon_returns.get(horizon, [])

        print()
        print(f"+{horizon}m")
        print(f"  observed: {statuses['OBSERVED']}")
        print(f"  unresolved: {statuses['UNRESOLVED']}")
        print(f"  censored: {statuses['CENSORED']}")

        if returns:
            print(f"  mean_return_pct: {mean(returns):+.2f}")
            print(f"  median_return_pct: {median(returns):+.2f}")
        else:
            print("  return_pct: N/A")


def main():
    with SAMPLE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)

        if not REQUIRED_FIELDS.issubset(reader.fieldnames or []):
            missing = REQUIRED_FIELDS - set(reader.fieldnames or [])
            raise ValueError(
                f"Sample CSV is missing required columns: {sorted(missing)}"
            )

        counts, horizon_returns, horizon_status = analyze(reader)

    print_summary(counts, horizon_returns, horizon_status)


if __name__ == "__main__":
    main()
