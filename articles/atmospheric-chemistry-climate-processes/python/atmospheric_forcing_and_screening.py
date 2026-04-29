#!/usr/bin/env python3
"""
Atmospheric chemistry workflow:
- Load synthetic atmospheric monitoring records.
- Compute screening ratios relative to selected references or benchmarks.
- Estimate approximate CO2 radiative forcing.
- Estimate first-order atmospheric decay for a short-lived species.
- Write reproducible tables, report, and provenance manifest.

Educational only. Not for air-quality compliance, climate attribution,
public-health advisories, or legal determinations.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "atmospheric_monitoring_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"


def parse_float(value: str) -> float | None:
    """Parse numbers while preserving blank/NA values as None."""
    value = value.strip()
    if value == "" or value.upper() == "NA":
        return None
    return float(value)


def load_rows() -> list[dict]:
    """Load synthetic atmospheric records."""
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        numeric_fields = [
            "latitude",
            "longitude",
            "altitude_m",
            "concentration",
            "reference_value",
            "temperature_c",
            "relative_humidity_percent",
            "wind_speed_m_s",
        ]

        for row in reader:
            for field in numeric_fields:
                row[field] = parse_float(row[field])
            rows.append(row)

        return rows


def screening_ratio(concentration: float | None, reference_value: float | None) -> float | None:
    """Compute a concentration/reference screening ratio."""
    if concentration is None or reference_value is None or reference_value <= 0:
        return None
    return concentration / reference_value


def add_screening(rows: list[dict]) -> list[dict]:
    """Add screening ratio and interpretive flag."""
    enriched = []
    for row in rows:
        ratio = screening_ratio(row["concentration"], row["reference_value"])
        item = dict(row)
        item["ratio_to_reference"] = ratio
        item["screening_flag"] = (
            "above_reference"
            if ratio is not None and ratio > 1.0
            else "at_or_below_reference"
        )
        enriched.append(item)
    return enriched


def co2_radiative_forcing(current_ppm: float, reference_ppm: float = 280.0) -> float:
    """
    Approximate CO2 radiative forcing.

    Delta F = 5.35 * ln(C / C0)
    Units: W/m2
    """
    return 5.35 * math.log(current_ppm / reference_ppm)


def first_order_decay(initial: float, k_per_day: float, duration_days: int, step_days: int) -> list[dict]:
    """
    First-order atmospheric lifetime model.

    C(t) = C0 * exp(-k t)
    tau = 1 / k
    t1/2 = ln(2) / k
    """
    lifetime = 1.0 / k_per_day
    half_life = math.log(2.0) / k_per_day
    rows = []

    for day in range(0, duration_days + 1, step_days):
        concentration = initial * math.exp(-k_per_day * day)
        rows.append(
            {
                "day": day,
                "mixing_ratio_ppb": concentration,
                "fraction_remaining": concentration / initial,
                "lifetime_days": lifetime,
                "half_life_days": half_life,
            }
        )

    return rows


def simplified_ozone_production_index(nox_ppb: float, voc_ppb: float, sunlight_index: float) -> float:
    """
    A pedagogical ozone-production index.

    This is not a chemical mechanism. It simply encodes the idea that
    ozone formation depends on precursor availability and sunlight.

    index = sunlight * sqrt(NOx * VOC)
    """
    return sunlight_index * math.sqrt(max(nox_ppb, 0.0) * max(voc_ppb, 0.0))


def class_summary(rows: list[dict]) -> list[dict]:
    """Summarize reference ratios by atmospheric chemical class."""
    groups: dict[str, list[float]] = {}
    for row in rows:
        ratio = row["ratio_to_reference"]
        if ratio is None:
            continue
        groups.setdefault(row["class"], []).append(ratio)

    summary = []
    for chemical_class, values in sorted(groups.items()):
        summary.append(
            {
                "class": chemical_class,
                "n": len(values),
                "mean_ratio_to_reference": mean(values),
                "max_ratio_to_reference": max(values),
                "above_reference_count": sum(value > 1.0 for value in values),
            }
        )

    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write dictionaries to CSV."""
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(screened: list[dict], decay: list[dict], forcing: float) -> None:
    """Write a concise Markdown report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    above = [row for row in screened if row["screening_flag"] == "above_reference"]

    lines = [
        "# Atmospheric Chemistry Screening Report",
        "",
        "This educational report summarizes synthetic atmospheric chemistry observations.",
        "",
        f"Total records: {len(screened)}",
        f"Records above selected reference or benchmark: {len(above)}",
        f"Approximate CO2 forcing relative to 280 ppm: {forcing:.2f} W/m2",
        "",
        "## Above-reference observations",
        "",
    ]

    for row in above:
        lines.append(
            f"- {row['site']} | {row['analyte']} | {row['concentration']} {row['unit']} | "
            f"ratio={row['ratio_to_reference']:.2f} | context={row['averaging_period']}"
        )

    lines.extend(
        [
            "",
            "## First-order atmospheric lifetime example",
            "",
            f"Initial mixing ratio: {decay[0]['mixing_ratio_ppb']:.2f} ppb",
            f"Final modeled mixing ratio: {decay[-1]['mixing_ratio_ppb']:.2f} ppb",
            f"Lifetime: {decay[0]['lifetime_days']:.2f} days",
            f"Half-life: {decay[0]['half_life_days']:.2f} days",
            "",
            "This report is educational and is not a compliance or climate-attribution product.",
        ]
    )

    (REPORT_DIR / "atmospheric_screening_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    """Write provenance manifest."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "atmospheric-chemistry-climate-processes",
        "workflow": "atmospheric_forcing_and_screening.py",
        "data_source": "synthetic educational atmospheric monitoring data",
        "generated_outputs": [
            "outputs/tables/screened_atmospheric_data.csv",
            "outputs/tables/atmospheric_class_summary.csv",
            "outputs/tables/first_order_atmospheric_decay.csv",
            "outputs/tables/ozone_production_index.csv",
            "outputs/reports/atmospheric_screening_report.md",
        ],
        "responsible_use": "Educational only; not for air-quality compliance, legal, climate-attribution, health, or emergency decisions.",
    }

    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    screened = add_screening(rows)
    summary = class_summary(screened)

    decay = first_order_decay(
        initial=100.0,
        k_per_day=0.20,
        duration_days=30,
        step_days=2,
    )

    forcing = co2_radiative_forcing(current_ppm=423.0, reference_ppm=280.0)

    ozone_index = [
        {
            "case": "low_NOx_low_VOC",
            "nox_ppb": 5.0,
            "voc_ppb": 20.0,
            "sunlight_index": 0.8,
            "ozone_production_index": simplified_ozone_production_index(5.0, 20.0, 0.8),
        },
        {
            "case": "urban_sunny",
            "nox_ppb": 35.0,
            "voc_ppb": 80.0,
            "sunlight_index": 1.0,
            "ozone_production_index": simplified_ozone_production_index(35.0, 80.0, 1.0),
        },
        {
            "case": "biogenic_hot_sunny",
            "nox_ppb": 12.0,
            "voc_ppb": 140.0,
            "sunlight_index": 1.2,
            "ozone_production_index": simplified_ozone_production_index(12.0, 140.0, 1.2),
        },
    ]

    write_csv(TABLE_DIR / "screened_atmospheric_data.csv", screened)
    write_csv(TABLE_DIR / "atmospheric_class_summary.csv", summary)
    write_csv(TABLE_DIR / "first_order_atmospheric_decay.csv", decay)
    write_csv(TABLE_DIR / "ozone_production_index.csv", ozone_index)
    write_report(screened, decay, forcing)
    write_manifest()

    print("Atmospheric chemistry workflow complete.")
    print(f"Approximate CO2 forcing: {forcing:.2f} W/m2")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
