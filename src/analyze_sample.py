"""Offline portfolio example. All bundled observations are synthetic."""

import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path
from statistics import mean, median


SAMPLE = Path(__file__).resolve().parents[1] / "samples" / "synthetic_observations.csv"
FIELDS = {"observation_id", "symbol", "observed_at", "reference_price", "later_price"}


def positive_price(value):
    """Return a finite positive decimal; reject malformed or missing prices."""
    try:
        number = Decimal(value.strip())
    except (InvalidOperation, AttributeError):
        return None
    return number if number.is_finite() and number > 0 else None


def summarize(rows):
    counts = Counter(total=0, duplicate=0, invalid_id=0, invalid_price=0, valid=0)
    seen = set()
    changes = []
    for row in rows:
        counts["total"] += 1
        identifier = (row.get("observation_id") or "").strip()
        if not identifier:
            counts["invalid_id"] += 1
            continue
        if identifier in seen:
            counts["duplicate"] += 1
            continue
        seen.add(identifier)
        before = positive_price(row.get("reference_price"))
        after = positive_price(row.get("later_price"))
        if before is None or after is None:
            counts["invalid_price"] += 1
            continue
        counts["valid"] += 1
        changes.append((after / before - 1) * 100)
    return counts, changes


def main():
    with SAMPLE.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not FIELDS.issubset(reader.fieldnames or []):
            raise ValueError("Sample CSV is missing required columns")
        counts, changes = summarize(reader)
    print("SYNTHETIC DATA DEMO - not real market results")
    for key in ("total", "duplicate", "invalid_id", "invalid_price", "valid"):
        print(f"{key}: {counts[key]}")
    if changes:
        print(f"mean_price_change_pct: {mean(changes):+.2f}")
        print(f"median_price_change_pct: {median(changes):+.2f}")
    else:
        print("price_change_pct: N/A (no valid observations)")


if __name__ == "__main__":
    main()
