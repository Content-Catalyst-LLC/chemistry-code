#!/usr/bin/env python3
"""
Geochemistry workflow:
- Load synthetic rock, sediment, and regolith geochemistry data.
- Calculate a simplified Chemical Index of Alteration.
- Calculate trace-element ratios.
- Calculate isotope delta notation examples.
- Estimate simplified parent-daughter radiometric ages.
- Write reproducible tables, report, and provenance manifest.

Educational only. Not for professional geochronology, mining, contamination,
legal, or resource-assessment use.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "geochemical_samples_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"


NUMERIC_FIELDS = [
    "SiO2_wt_pct",
    "Al2O3_wt_pct",
    "FeO_total_wt_pct",
    "MgO_wt_pct",
    "CaO_wt_pct",
    "Na2O_wt_pct",
    "K2O_wt_pct",
    "TiO2_wt_pct",
    "P2O5_wt_pct",
    "Rb_ppm",
    "Sr_ppm",
    "Zr_ppm",
    "Y_ppm",
    "La_ppm",
    "Ce_ppm",
    "Nd_ppm",
    "U_ppm",
    "Th_ppm",
    "parent_isotope_units",
    "radiogenic_daughter_units",
    "delta13C_permil",
    "delta18O_permil",
    "latitude",
    "longitude",
]


def parse_float(value: str) -> float | None:
    """Parse numeric fields while preserving missing values."""
    value = value.strip()
    if value == "" or value.upper() == "NA":
        return None
    return float(value)


def load_rows() -> list[dict]:
    """Load synthetic geochemical records."""
    rows = []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for field in NUMERIC_FIELDS:
                row[field] = parse_float(row[field])
            rows.append(row)
    return rows


def simplified_cia(row: dict) -> float | None:
    """
    Simplified Chemical Index of Alteration.

    CIA = 100 * Al2O3 / (Al2O3 + CaO + Na2O + K2O)

    This teaching calculation uses oxide weight percentages and does not
    convert to molar proportions or correct CaO*. Research workflows should.
    """
    values = [row["Al2O3_wt_pct"], row["CaO_wt_pct"], row["Na2O_wt_pct"], row["K2O_wt_pct"]]
    if any(value is None for value in values):
        return None

    denominator = row["Al2O3_wt_pct"] + row["CaO_wt_pct"] + row["Na2O_wt_pct"] + row["K2O_wt_pct"]
    if denominator <= 0:
        return None
    return 100.0 * row["Al2O3_wt_pct"] / denominator


def ratio(numerator: float | None, denominator: float | None) -> float | None:
    """Safe element-ratio calculation."""
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def radiometric_age_ma(parent: float | None, daughter: float | None, decay_constant_per_year: float) -> float | None:
    """
    Simplified parent-daughter radiometric age.

    t = (1/lambda) * ln(1 + D/P)

    Assumes no initial daughter and a closed system.
    """
    if parent is None or daughter is None or parent <= 0:
        return None

    age_years = (1.0 / decay_constant_per_year) * math.log(1.0 + daughter / parent)
    return age_years / 1.0e6


def delta_from_ratios(sample_ratio: float, standard_ratio: float) -> float:
    """
    Delta notation.

    delta = ((R_sample / R_standard) - 1) * 1000
    """
    return ((sample_ratio / standard_ratio) - 1.0) * 1000.0


def add_geochemical_indicators(rows: list[dict]) -> list[dict]:
    """Add geochemical indicators to each record."""
    enriched = []
    decay_constant = 1.55125e-10  # illustrative U-238-like decay constant per year

    for row in rows:
        item = dict(row)
        item["CIA_simplified"] = simplified_cia(row)
        item["Rb_Sr_ratio"] = ratio(row["Rb_ppm"], row["Sr_ppm"])
        item["Th_U_ratio"] = ratio(row["Th_ppm"], row["U_ppm"])
        item["Zr_Y_ratio"] = ratio(row["Zr_ppm"], row["Y_ppm"])
        item["La_Y_ratio"] = ratio(row["La_ppm"], row["Y_ppm"])
        item["radiometric_age_Ma_simplified"] = radiometric_age_ma(
            row["parent_isotope_units"],
            row["radiogenic_daughter_units"],
            decay_constant,
        )
        item["weathering_screen"] = (
            "strong_weathering_screen"
            if item["CIA_simplified"] is not None and item["CIA_simplified"] > 80
            else "moderate_or_low_screen"
        )
        item["redox_archive_screen"] = (
            "redox_sensitive_archive"
            if row["rock_type"] in {"banded_iron_formation", "shale", "sulfide"}
            else "general_geochemical_archive"
        )
        enriched.append(item)

    return enriched


def summarize_by_rock_type(rows: list[dict]) -> list[dict]:
    """Summarize geochemical indicators by rock type."""
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row["rock_type"], []).append(row)

    summary = []
    for rock_type, records in sorted(groups.items()):
        summary.append(
            {
                "rock_type": rock_type,
                "n": len(records),
                "mean_SiO2_wt_pct": mean(row["SiO2_wt_pct"] for row in records if row["SiO2_wt_pct"] is not None),
                "mean_CIA_simplified": mean(row["CIA_simplified"] for row in records if row["CIA_simplified"] is not None),
                "mean_Rb_Sr_ratio": mean(row["Rb_Sr_ratio"] for row in records if row["Rb_Sr_ratio"] is not None),
                "mean_radiometric_age_Ma_simplified": mean(
                    row["radiometric_age_Ma_simplified"]
                    for row in records
                    if row["radiometric_age_Ma_simplified"] is not None
                ),
            }
        )

    return summary


def isotope_delta_examples() -> list[dict]:
    """Create small isotope delta notation examples."""
    standard_c = 0.01118
    standard_o = 0.0020052

    examples = [
        {
            "system": "carbon",
            "sample_ratio": 0.01112,
            "standard_ratio": standard_c,
            "delta_permil": delta_from_ratios(0.01112, standard_c),
        },
        {
            "system": "oxygen",
            "sample_ratio": 0.002021,
            "standard_ratio": standard_o,
            "delta_permil": delta_from_ratios(0.002021, standard_o),
        },
    ]

    return examples


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


def write_report(rows: list[dict], summary: list[dict]) -> None:
    """Write concise Markdown report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    strong_weathering = [row for row in rows if row["weathering_screen"] == "strong_weathering_screen"]
    redox_archives = [row for row in rows if row["redox_archive_screen"] == "redox_sensitive_archive"]

    lines = [
        "# Geochemistry Screening Report",
        "",
        "This educational report summarizes synthetic geochemical records.",
        "",
        f"Total samples: {len(rows)}",
        f"Strong weathering screens: {len(strong_weathering)}",
        f"Redox-sensitive archive screens: {len(redox_archives)}",
        "",
        "## Strong weathering screens",
        "",
    ]

    for row in strong_weathering:
        lines.append(
            f"- {row['sample_id']} | {row['rock_type']} | CIA={row['CIA_simplified']:.2f}"
        )

    lines.extend(
        [
            "",
            "## Redox-sensitive archive screens",
            "",
        ]
    )

    for row in redox_archives:
        lines.append(
            f"- {row['sample_id']} | {row['rock_type']} | context={row['geologic_context']}"
        )

    lines.extend(
        [
            "",
            "## Rock-type summary",
            "",
        ]
    )

    for row in summary:
        lines.append(
            f"- {row['rock_type']} | mean SiO2={row['mean_SiO2_wt_pct']:.2f} wt% | "
            f"mean CIA={row['mean_CIA_simplified']:.2f}"
        )

    lines.extend(
        [
            "",
            "This report is educational and is not a professional geochemical interpretation, resource estimate, contamination assessment, legal determination, or geochronology report.",
        ]
    )

    (REPORT_DIR / "geochemistry_screening_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    """Write provenance manifest."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "geochemistry-chemical-history-earth",
        "workflow": "geochemistry_indices_and_ages.py",
        "data_source": "synthetic educational geochemical data",
        "generated_outputs": [
            "outputs/tables/geochemical_indicators.csv",
            "outputs/tables/rock_type_summary.csv",
            "outputs/tables/isotope_delta_examples.csv",
            "outputs/reports/geochemistry_screening_report.md",
        ],
        "responsible_use": "Educational only; not for resource assessment, mining decisions, professional geochronology, contamination assessment, legal, or regulatory decisions.",
    }

    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = add_geochemical_indicators(rows)
    summary = summarize_by_rock_type(indicators)
    isotope_examples = isotope_delta_examples()

    write_csv(TABLE_DIR / "geochemical_indicators.csv", indicators)
    write_csv(TABLE_DIR / "rock_type_summary.csv", summary)
    write_csv(TABLE_DIR / "isotope_delta_examples.csv", isotope_examples)
    write_report(indicators, summary)
    write_manifest()

    print("Geochemistry workflow complete.")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
