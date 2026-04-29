#!/usr/bin/env python3
"""
Soil chemistry workflow:
- Load synthetic soil monitoring data.
- Estimate soil organic carbon stocks.
- Compute base saturation.
- Flag acidic soils, elevated salinity screens, high phosphorus, high nitrate,
  and contaminant attention values.
- Write reproducible tables, report, and provenance manifest.

Educational only. Not for agronomic recommendations, legal determinations,
contamination assessment, carbon-credit verification, or public-health decisions.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "soil_monitoring_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"


NUMERIC_FIELDS = [
    "depth_cm",
    "bulk_density_g_cm3",
    "pH",
    "electrical_conductivity_dS_m",
    "soil_organic_carbon_percent",
    "nitrate_mg_kg",
    "ammonium_mg_kg",
    "phosphorus_mg_kg",
    "potassium_mg_kg",
    "cec_cmolc_kg",
    "base_cations_cmolc_kg",
    "clay_percent",
    "sand_percent",
    "silt_percent",
    "lead_mg_kg",
    "cadmium_mg_kg",
    "latitude",
    "longitude",
]


def parse_float(value: str) -> float | None:
    """Parse numeric fields while preserving blanks and NA values."""
    value = value.strip()
    if value == "" or value.upper() == "NA":
        return None
    return float(value)


def load_rows() -> list[dict]:
    """Load synthetic soil monitoring data."""
    rows = []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for field in NUMERIC_FIELDS:
                row[field] = parse_float(row[field])
            rows.append(row)
    return rows


def soc_stock_mg_ha(soc_percent: float | None, bulk_density: float | None, depth_cm: float | None) -> float | None:
    """
    Estimate soil organic carbon stock.

    Practical expression:
    Mg C/ha = SOC_percent * bulk_density_g_cm3 * depth_cm
    """
    if soc_percent is None or bulk_density is None or depth_cm is None:
        return None
    return soc_percent * bulk_density * depth_cm


def base_saturation_percent(base_cations: float | None, cec: float | None) -> float | None:
    """Estimate base saturation percentage."""
    if base_cations is None or cec is None or cec <= 0:
        return None
    return 100.0 * base_cations / cec


def add_screening_fields(rows: list[dict]) -> list[dict]:
    """Add soil chemistry calculations and screening flags."""
    enriched = []

    for row in rows:
        item = dict(row)
        item["soc_stock_Mg_ha"] = soc_stock_mg_ha(
            row["soil_organic_carbon_percent"],
            row["bulk_density_g_cm3"],
            row["depth_cm"],
        )
        item["base_saturation_percent"] = base_saturation_percent(
            row["base_cations_cmolc_kg"],
            row["cec_cmolc_kg"],
        )

        item["pH_flag"] = "acidic_screen" if row["pH"] is not None and row["pH"] < 5.8 else "not_acidic_screen"
        item["salinity_flag"] = (
            "elevated_salinity_screen"
            if row["electrical_conductivity_dS_m"] is not None and row["electrical_conductivity_dS_m"] > 1.2
            else "not_elevated_screen"
        )
        item["phosphorus_flag"] = (
            "high_phosphorus_runoff_attention"
            if row["phosphorus_mg_kg"] is not None and row["phosphorus_mg_kg"] > 60
            else "not_high_screen"
        )
        item["nitrate_flag"] = (
            "high_nitrate_leaching_attention"
            if row["nitrate_mg_kg"] is not None and row["nitrate_mg_kg"] > 30
            else "not_high_screen"
        )
        item["lead_flag"] = (
            "lead_attention_screen"
            if row["lead_mg_kg"] is not None and row["lead_mg_kg"] > 400
            else "not_high_screen"
        )
        item["cadmium_flag"] = (
            "cadmium_attention_screen"
            if row["cadmium_mg_kg"] is not None and row["cadmium_mg_kg"] > 3
            else "not_high_screen"
        )

        enriched.append(item)

    return enriched


def summarize_by_land_use(rows: list[dict]) -> list[dict]:
    """Summarize soil chemistry indicators by land use."""
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row["land_use"], []).append(row)

    summary = []
    for land_use, records in sorted(groups.items()):
        summary.append(
            {
                "land_use": land_use,
                "n": len(records),
                "mean_pH": mean(row["pH"] for row in records if row["pH"] is not None),
                "mean_SOC_percent": mean(
                    row["soil_organic_carbon_percent"]
                    for row in records
                    if row["soil_organic_carbon_percent"] is not None
                ),
                "mean_SOC_stock_Mg_ha": mean(
                    row["soc_stock_Mg_ha"]
                    for row in records
                    if row["soc_stock_Mg_ha"] is not None
                ),
                "mean_CEC_cmolc_kg": mean(
                    row["cec_cmolc_kg"]
                    for row in records
                    if row["cec_cmolc_kg"] is not None
                ),
            }
        )

    return summary


def nitrogen_balance_example() -> list[dict]:
    """Create a simple synthetic nitrogen balance table."""
    balances = [
        {
            "field": "Field-A",
            "fertilizer_N_kg_ha": 135,
            "manure_N_kg_ha": 0,
            "fixation_N_kg_ha": 25,
            "harvest_removal_N_kg_ha": 118,
            "leaching_loss_N_kg_ha": 18,
            "gaseous_loss_N_kg_ha": 12,
        },
        {
            "field": "Field-B",
            "fertilizer_N_kg_ha": 165,
            "manure_N_kg_ha": 35,
            "fixation_N_kg_ha": 20,
            "harvest_removal_N_kg_ha": 145,
            "leaching_loss_N_kg_ha": 28,
            "gaseous_loss_N_kg_ha": 22,
        },
    ]

    for row in balances:
        row["net_N_kg_ha"] = (
            row["fertilizer_N_kg_ha"]
            + row["manure_N_kg_ha"]
            + row["fixation_N_kg_ha"]
            - row["harvest_removal_N_kg_ha"]
            - row["leaching_loss_N_kg_ha"]
            - row["gaseous_loss_N_kg_ha"]
        )

    return balances


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


def write_report(rows: list[dict], balances: list[dict]) -> None:
    """Write a concise Markdown report."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    acidic = [row for row in rows if row["pH_flag"] == "acidic_screen"]
    high_p = [row for row in rows if row["phosphorus_flag"] == "high_phosphorus_runoff_attention"]
    high_n = [row for row in rows if row["nitrate_flag"] == "high_nitrate_leaching_attention"]
    metals = [
        row for row in rows
        if row["lead_flag"] == "lead_attention_screen" or row["cadmium_flag"] == "cadmium_attention_screen"
    ]

    lines = [
        "# Soil Chemistry Monitoring Report",
        "",
        "This educational report summarizes synthetic soil monitoring records.",
        "",
        f"Total samples: {len(rows)}",
        f"Acidic screen flags: {len(acidic)}",
        f"High phosphorus attention flags: {len(high_p)}",
        f"High nitrate attention flags: {len(high_n)}",
        f"Metal attention flags: {len(metals)}",
        "",
        "## Attention flags",
        "",
    ]

    for row in acidic + high_p + high_n + metals:
        lines.append(
            f"- {row['site']} | {row['land_use']} | pH={row['pH']} | "
            f"P={row['phosphorus_mg_kg']} mg/kg | nitrate={row['nitrate_mg_kg']} mg/kg | "
            f"lead={row['lead_mg_kg']} mg/kg | cadmium={row['cadmium_mg_kg']} mg/kg"
        )

    lines.extend(
        [
            "",
            "## Nitrogen balance examples",
            "",
        ]
    )

    for row in balances:
        lines.append(
            f"- {row['field']} | net nitrogen balance = {row['net_N_kg_ha']} kg/ha"
        )

    lines.extend(
        [
            "",
            "This report is educational and is not an agronomic recommendation, soil-carbon verification, contamination assessment, legal determination, or public-health advisory.",
        ]
    )

    (REPORT_DIR / "soil_chemistry_screening_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    """Write provenance manifest."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "soil-chemistry-nutrient-cycles-land-systems",
        "workflow": "soil_fertility_and_carbon.py",
        "data_source": "synthetic educational soil monitoring data",
        "generated_outputs": [
            "outputs/tables/screened_soil_monitoring_data.csv",
            "outputs/tables/soil_land_use_summary.csv",
            "outputs/tables/nitrogen_balance_examples.csv",
            "outputs/reports/soil_chemistry_screening_report.md",
        ],
        "responsible_use": "Educational only; not for agronomic, regulatory, soil-carbon-credit, contamination, legal, or public-health decisions.",
    }

    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    screened = add_screening_fields(rows)
    summary = summarize_by_land_use(screened)
    balances = nitrogen_balance_example()

    write_csv(TABLE_DIR / "screened_soil_monitoring_data.csv", screened)
    write_csv(TABLE_DIR / "soil_land_use_summary.csv", summary)
    write_csv(TABLE_DIR / "nitrogen_balance_examples.csv", balances)
    write_report(screened, balances)
    write_manifest()

    print("Soil chemistry workflow complete.")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
