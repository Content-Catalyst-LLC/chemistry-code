#!/usr/bin/env python3
"""
Environmental chemistry workflow:
- Load synthetic monitoring data.
- Compute benchmark screening ratios.
- Estimate first-order environmental fate after a pulse release.
- Write reproducible output tables and a provenance manifest.

This script is educational and not intended for regulatory decision-making.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "environmental_monitoring_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"


def parse_float(value: str) -> float | None:
    """Parse numeric fields while preserving NA as None."""
    if value.strip().upper() == "NA":
        return None
    return float(value)


def load_monitoring_rows() -> list[dict]:
    """Load synthetic monitoring records from CSV."""
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            row["concentration"] = parse_float(row["concentration"])
            row["benchmark"] = parse_float(row["benchmark"])
            row["pH"] = parse_float(row["pH"])
            row["temperature_c"] = parse_float(row["temperature_c"])
            row["flow_L_s"] = parse_float(row["flow_L_s"])
            rows.append(row)
        return rows


def add_screening_fields(rows: list[dict]) -> list[dict]:
    """Compute hazard quotient and benchmark flag for each record."""
    enriched = []
    for row in rows:
        concentration = row["concentration"]
        benchmark = row["benchmark"]
        hazard_quotient = concentration / benchmark if benchmark and benchmark > 0 else None

        enriched_row = dict(row)
        enriched_row["hazard_quotient"] = hazard_quotient
        enriched_row["screening_flag"] = (
            "exceeds_benchmark"
            if hazard_quotient is not None and hazard_quotient > 1.0
            else "below_benchmark"
        )
        enriched.append(enriched_row)
    return enriched


def first_order_decay(
    initial_concentration: float,
    rate_constant_per_day: float,
    duration_days: int,
    step_days: int,
) -> list[dict]:
    """
    Generate a first-order decay curve.

    C(t) = C0 * exp(-k * t)
    t1/2 = ln(2) / k
    """
    rows = []
    half_life = math.log(2.0) / rate_constant_per_day

    for day in range(0, duration_days + 1, step_days):
        concentration = initial_concentration * math.exp(-rate_constant_per_day * day)
        rows.append(
            {
                "day": day,
                "concentration_ug_L": concentration,
                "fraction_remaining": concentration / initial_concentration,
                "half_life_days": half_life,
            }
        )

    return rows


def summarize_by_medium(rows: list[dict]) -> list[dict]:
    """Summarize hazard quotient by environmental medium."""
    groups: dict[str, list[float]] = {}
    for row in rows:
        hq = row["hazard_quotient"]
        if hq is None:
            continue
        groups.setdefault(row["medium"], []).append(hq)

    summary = []
    for medium, values in sorted(groups.items()):
        summary.append(
            {
                "medium": medium,
                "n": len(values),
                "mean_hazard_quotient": mean(values),
                "max_hazard_quotient": max(values),
                "exceedance_count": sum(value > 1.0 for value in values),
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write a list of dictionaries to CSV."""
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(screened_rows: list[dict], decay_rows: list[dict]) -> None:
    """Write a concise Markdown report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    exceedances = [row for row in screened_rows if row["screening_flag"] == "exceeds_benchmark"]

    lines = [
        "# Environmental Chemistry Screening Report",
        "",
        "This educational report summarizes synthetic environmental monitoring records.",
        "",
        f"Total records: {len(screened_rows)}",
        f"Benchmark exceedances: {len(exceedances)}",
        "",
        "## Exceedances",
        "",
    ]

    for row in exceedances:
        lines.append(
            f"- {row['site']} | {row['medium']} | {row['analyte']} | "
            f"HQ={row['hazard_quotient']:.2f} | {row['concentration']} {row['unit']}"
        )

    lines.extend(
        [
            "",
            "## First-order persistence example",
            "",
            f"Initial concentration: {decay_rows[0]['concentration_ug_L']:.2f} ug/L",
            f"Final modeled concentration: {decay_rows[-1]['concentration_ug_L']:.2f} ug/L",
            f"Half-life: {decay_rows[0]['half_life_days']:.2f} days",
            "",
            "This report is not a regulatory determination.",
        ]
    )

    (REPORT_DIR / "environmental_screening_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    """Write a small provenance manifest."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "environmental-chemistry-chemical-conditions-habitability",
        "workflow": "environmental_fate_and_screening.py",
        "data_source": "synthetic educational data",
        "generated_outputs": [
            "outputs/tables/screened_monitoring_data.csv",
            "outputs/tables/medium_summary.csv",
            "outputs/tables/first_order_decay_curve.csv",
            "outputs/reports/environmental_screening_report.md",
        ],
        "responsible_use": "Educational only; not for compliance, legal, clinical, or emergency decisions.",
    }
    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_monitoring_rows()
    screened = add_screening_fields(rows)
    summary = summarize_by_medium(screened)
    decay = first_order_decay(
        initial_concentration=100.0,
        rate_constant_per_day=0.08,
        duration_days=90,
        step_days=5,
    )

    write_csv(TABLE_DIR / "screened_monitoring_data.csv", screened)
    write_csv(TABLE_DIR / "medium_summary.csv", summary)
    write_csv(TABLE_DIR / "first_order_decay_curve.csv", decay)
    write_report(screened, decay)
    write_manifest()

    print("Environmental chemistry workflow complete.")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
