#!/usr/bin/env python3
"""
Water chemistry workflow:
- Load synthetic water-quality monitoring records.
- Compute benchmark screening ratios.
- Estimate nutrient loads from concentration and flow.
- Flag pH values outside an illustrative aquatic-life range.
- Write output tables, report, and provenance manifest.

Educational only. Not for regulatory, drinking-water, legal, emergency,
or public-health determinations.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "water_quality_monitoring_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"


def parse_float(value: str) -> float | None:
    """Parse numeric fields while preserving NA as None."""
    value = value.strip()
    if value == "" or value.upper() == "NA":
        return None
    return float(value)


def load_rows() -> list[dict]:
    """Load synthetic water-quality records."""
    numeric_fields = [
        "concentration",
        "benchmark",
        "pH",
        "temperature_c",
        "conductivity_uS_cm",
        "flow_L_s",
        "latitude",
        "longitude",
    ]

    rows = []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for field in numeric_fields:
                row[field] = parse_float(row[field])
            row["filtered"] = str(row["filtered"]).lower() == "true"
            rows.append(row)

    return rows


def ratio_to_benchmark(concentration: float | None, benchmark: float | None) -> float | None:
    """Compute concentration/benchmark ratio."""
    if concentration is None or benchmark is None or benchmark <= 0:
        return None
    return concentration / benchmark


def nutrient_load_kg_day(analyte: str, concentration: float | None, unit: str, flow_l_s: float | None) -> float | None:
    """
    Estimate nutrient load for mg/L nutrient concentrations.

    kg/day = mg/L * L/s * 0.0864

    This only applies to nutrients reported in mg/L and requires flow.
    """
    nutrient_names = {"nitrate_as_N", "phosphate_as_P", "total_phosphorus", "ammonia_as_N"}
    if analyte not in nutrient_names:
        return None
    if unit != "mg/L" or concentration is None or flow_l_s is None:
        return None
    return concentration * flow_l_s * 0.0864


def ph_flag(value: float | None) -> str:
    """Flag pH outside an illustrative aquatic-life range."""
    if value is None:
        return "missing_pH"
    if value < 6.5 or value > 9.0:
        return "outside_illustrative_aquatic_range"
    return "within_illustrative_aquatic_range"


def add_screening_fields(rows: list[dict]) -> list[dict]:
    """Add benchmark ratio, screening flag, pH flag, and nutrient load."""
    enriched = []

    for row in rows:
        ratio = ratio_to_benchmark(row["concentration"], row["benchmark"])
        item = dict(row)
        item["ratio_to_benchmark"] = ratio
        item["screening_flag"] = (
            "exceeds_benchmark"
            if ratio is not None and ratio > 1.0
            else "below_benchmark"
        )
        item["pH_flag"] = ph_flag(row["pH"])
        item["load_kg_day"] = nutrient_load_kg_day(
            row["analyte"],
            row["concentration"],
            row["unit"],
            row["flow_L_s"],
        )
        enriched.append(item)

    return enriched


def summarize_by_medium(rows: list[dict]) -> list[dict]:
    """Summarize benchmark ratios by medium."""
    groups: dict[str, list[float]] = {}

    for row in rows:
        ratio = row["ratio_to_benchmark"]
        if ratio is None:
            continue
        groups.setdefault(row["medium"], []).append(ratio)

    summary = []
    for medium, values in sorted(groups.items()):
        summary.append(
            {
                "medium": medium,
                "n": len(values),
                "mean_ratio_to_benchmark": mean(values),
                "max_ratio_to_benchmark": max(values),
                "exceedance_count": sum(value > 1.0 for value in values),
            }
        )

    return summary


def summarize_nutrient_loads(rows: list[dict]) -> list[dict]:
    """Extract nutrient load rows."""
    nutrient_rows = []

    for row in rows:
        load = row["load_kg_day"]
        if load is not None:
            nutrient_rows.append(
                {
                    "sample_id": row["sample_id"],
                    "site": row["site"],
                    "analyte": row["analyte"],
                    "concentration": row["concentration"],
                    "unit": row["unit"],
                    "flow_L_s": row["flow_L_s"],
                    "load_kg_day": load,
                }
            )

    return nutrient_rows


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


def write_report(screened_rows: list[dict], nutrient_rows: list[dict]) -> None:
    """Write a concise Markdown report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    exceedances = [row for row in screened_rows if row["screening_flag"] == "exceeds_benchmark"]
    ph_flags = [row for row in screened_rows if row["pH_flag"] == "outside_illustrative_aquatic_range"]

    total_n_load = sum(
        row["load_kg_day"]
        for row in nutrient_rows
        if row["analyte"] in {"nitrate_as_N", "ammonia_as_N"}
    )
    total_p_load = sum(
        row["load_kg_day"]
        for row in nutrient_rows
        if row["analyte"] in {"phosphate_as_P", "total_phosphorus"}
    )

    lines = [
        "# Water Chemistry Monitoring Report",
        "",
        "This educational report summarizes synthetic water-quality monitoring records.",
        "",
        f"Total records: {len(screened_rows)}",
        f"Benchmark exceedances: {len(exceedances)}",
        f"pH values outside illustrative aquatic range: {len(ph_flags)}",
        f"Estimated nitrogen load in synthetic nutrient rows: {total_n_load:.2f} kg/day",
        f"Estimated phosphorus load in synthetic nutrient rows: {total_p_load:.2f} kg/day",
        "",
        "## Benchmark exceedances",
        "",
    ]

    for row in exceedances:
        lines.append(
            f"- {row['site']} | {row['medium']} | {row['analyte']} | "
            f"{row['concentration']} {row['unit']} | ratio={row['ratio_to_benchmark']:.2f}"
        )

    lines.extend(
        [
            "",
            "## pH flags",
            "",
        ]
    )

    for row in ph_flags:
        lines.append(
            f"- {row['site']} | pH={row['pH']} | {row['pH_flag']}"
        )

    lines.extend(
        [
            "",
            "This report is educational and is not a regulatory, drinking-water, legal, or public-health determination.",
        ]
    )

    (REPORT_DIR / "water_quality_screening_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    """Write provenance manifest."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "water-chemistry-environmental-monitoring",
        "workflow": "water_quality_screening.py",
        "data_source": "synthetic educational water-quality monitoring data",
        "generated_outputs": [
            "outputs/tables/screened_water_quality_data.csv",
            "outputs/tables/water_medium_summary.csv",
            "outputs/tables/nutrient_loads.csv",
            "outputs/reports/water_quality_screening_report.md",
        ],
        "responsible_use": "Educational only; not for regulatory, drinking-water, legal, public-health, or emergency decisions.",
    }
    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    screened = add_screening_fields(rows)
    medium_summary = summarize_by_medium(screened)
    nutrient_loads = summarize_nutrient_loads(screened)

    write_csv(TABLE_DIR / "screened_water_quality_data.csv", screened)
    write_csv(TABLE_DIR / "water_medium_summary.csv", medium_summary)
    write_csv(TABLE_DIR / "nutrient_loads.csv", nutrient_loads)
    write_report(screened, nutrient_loads)
    write_manifest()

    print("Water chemistry monitoring workflow complete.")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
