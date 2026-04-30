#!/usr/bin/env python3
"""
Advanced soil chemistry workflow.

Article:
Soil Chemistry, Nutrient Cycles, and Land Systems

This script uses synthetic soil monitoring data to calculate:

- soil organic carbon stock
- equivalent soil mass proxy
- cation exchange and base saturation
- exchange acidity proxy
- nitrate leaching vulnerability
- phosphorus export proxy
- nitrogen and phosphorus balance
- pH, salinity, nutrient, and contaminant flags
- soil land-system pressure index
- soil carbon scenario series
- nitrogen balance scenario series
- phosphorus export scenario series
- grouped summaries by land use

This is educational scaffolding only. It is not an agronomic recommendation
system, soil-carbon credit tool, contamination assessment, public-health
advisory, legal analysis, or regulatory reporting system.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "soil_chemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "depth_cm",
    "bulk_density_g_cm3",
    "soc_percent",
    "pH",
    "cec_cmolc_kg",
    "base_cations_cmolc_kg",
    "nitrate_mg_kg",
    "ammonium_mg_kg",
    "phosphorus_mg_kg",
    "potassium_mg_kg",
    "clay_percent",
    "sand_percent",
    "silt_percent",
    "electrical_conductivity_dS_m",
    "erosion_t_ha",
    "sediment_p_mg_kg",
    "lead_mg_kg",
    "cadmium_mg_kg",
    "annual_N_input_kg_ha",
    "annual_N_removal_kg_ha",
    "annual_P_input_kg_ha",
    "annual_P_removal_kg_ha",
    "qc_score",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp a value to a closed interval."""
    return max(low, min(high, value))


def parse_value(key: str, value: str):
    """Parse CSV values into numbers where appropriate."""
    if key in NUMERIC_FIELDS:
        return float(value)
    return value


def load_rows(path: Path = DATA_FILE) -> list[dict]:
    """Load synthetic soil monitoring records."""
    rows: list[dict] = []

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(key, value) for key, value in row.items()})

    return rows


def soc_stock_mg_ha(soc_percent: float, bulk_density_g_cm3: float, depth_cm: float) -> float:
    """
    Estimate soil organic carbon stock.

    Practical teaching expression:
    Mg C/ha = SOC_percent * bulk_density_g_cm3 * depth_cm
    """
    return soc_percent * bulk_density_g_cm3 * depth_cm


def equivalent_soil_mass_proxy(bulk_density_g_cm3: float, depth_cm: float) -> float:
    """
    Equivalent soil mass proxy.

    This is a simple mass-per-area proxy, not a full equivalent-soil-mass
    carbon accounting method.
    """
    return bulk_density_g_cm3 * depth_cm * 100.0


def base_saturation_percent(base_cations_cmolc_kg: float, cec_cmolc_kg: float) -> float:
    """Estimate base saturation percentage."""
    if cec_cmolc_kg <= 0:
        return 0.0
    return 100.0 * base_cations_cmolc_kg / cec_cmolc_kg


def exchange_acidity_proxy(cec_cmolc_kg: float, base_cations_cmolc_kg: float) -> float:
    """Estimate exchange acidity as CEC minus base cations."""
    return max(cec_cmolc_kg - base_cations_cmolc_kg, 0.0)


def texture_leaching_factor(sand_percent: float, clay_percent: float) -> float:
    """
    Estimate a texture-based leaching factor.

    Sandy soils receive higher leaching vulnerability; clay-rich soils receive
    lower values. This is a teaching proxy, not a hydrologic model.
    """
    return clamp((sand_percent - 0.5 * clay_percent) / 70.0)


def nitrate_leaching_vulnerability(row: dict) -> float:
    """Build a simplified nitrate leaching vulnerability index."""
    nitrate_pressure = clamp(row["nitrate_mg_kg"] / 50.0)
    texture_factor = texture_leaching_factor(row["sand_percent"], row["clay_percent"])
    low_cec_factor = clamp((15.0 - row["cec_cmolc_kg"]) / 15.0)
    qc_penalty = 1.0 - row["qc_score"]

    return clamp(
        0.45 * nitrate_pressure
        + 0.30 * texture_factor
        + 0.15 * low_cec_factor
        + 0.10 * qc_penalty
    )


def phosphorus_export_proxy(erosion_t_ha: float, sediment_p_mg_kg: float) -> float:
    """
    Estimate particulate phosphorus export proxy.

    kg P/ha = erosion_t_ha * sediment_p_mg_kg / 1000

    This assumes sediment P concentration and erosion mass are compatible.
    """
    return erosion_t_ha * sediment_p_mg_kg / 1000.0


def nutrient_balance(input_kg_ha: float, removal_kg_ha: float) -> float:
    """Simple annual nutrient balance."""
    return input_kg_ha - removal_kg_ha


def salinity_pressure(electrical_conductivity_dS_m: float) -> float:
    """Simplified soil salinity pressure."""
    return clamp((electrical_conductivity_dS_m - 0.7) / 2.0)


def pH_pressure(pH: float) -> float:
    """Simplified pH pressure from acidic or alkaline conditions."""
    if pH < 5.8:
        return clamp((5.8 - pH) / 1.5)
    if pH > 8.0:
        return clamp((pH - 8.0) / 1.5)
    return 0.0


def contaminant_pressure(row: dict) -> float:
    """Simplified contaminant pressure using lead and cadmium screens."""
    lead_component = clamp(row["lead_mg_kg"] / 400.0)
    cadmium_component = clamp(row["cadmium_mg_kg"] / 3.0)
    return clamp(0.6 * lead_component + 0.4 * cadmium_component)


def soil_land_system_pressure_index(row: dict) -> float:
    """
    Composite soil chemistry pressure index.

    Components:
    - pH pressure
    - nitrate leaching vulnerability
    - phosphorus export pressure
    - salinity pressure
    - contaminant pressure
    - low data quality
    """
    p_export = phosphorus_export_proxy(row["erosion_t_ha"], row["sediment_p_mg_kg"])

    return clamp(
        0.20 * pH_pressure(row["pH"])
        + 0.22 * nitrate_leaching_vulnerability(row)
        + 0.18 * clamp(p_export / 8.0)
        + 0.12 * salinity_pressure(row["electrical_conductivity_dS_m"])
        + 0.20 * contaminant_pressure(row)
        + 0.08 * (1.0 - row["qc_score"])
    )


def enrich_row(row: dict) -> dict:
    """Add advanced soil chemistry indicators to one row."""
    soc_stock = soc_stock_mg_ha(
        row["soc_percent"],
        row["bulk_density_g_cm3"],
        row["depth_cm"],
    )

    esm = equivalent_soil_mass_proxy(
        row["bulk_density_g_cm3"],
        row["depth_cm"],
    )

    base_sat = base_saturation_percent(
        row["base_cations_cmolc_kg"],
        row["cec_cmolc_kg"],
    )

    exchange_acidity = exchange_acidity_proxy(
        row["cec_cmolc_kg"],
        row["base_cations_cmolc_kg"],
    )

    p_export = phosphorus_export_proxy(
        row["erosion_t_ha"],
        row["sediment_p_mg_kg"],
    )

    n_balance = nutrient_balance(
        row["annual_N_input_kg_ha"],
        row["annual_N_removal_kg_ha"],
    )

    p_balance = nutrient_balance(
        row["annual_P_input_kg_ha"],
        row["annual_P_removal_kg_ha"],
    )

    nitrate_vulnerability = nitrate_leaching_vulnerability(row)
    pressure = soil_land_system_pressure_index(row)

    if pressure >= 0.65:
        attention_flag = "high_attention"
    elif pressure >= 0.45:
        attention_flag = "moderate_attention"
    else:
        attention_flag = "monitor"

    return {
        **row,
        "soc_stock_Mg_ha": soc_stock,
        "equivalent_soil_mass_proxy_Mg_ha": esm,
        "base_saturation_percent": base_sat,
        "exchange_acidity_proxy_cmolc_kg": exchange_acidity,
        "texture_leaching_factor": texture_leaching_factor(row["sand_percent"], row["clay_percent"]),
        "nitrate_leaching_vulnerability": nitrate_vulnerability,
        "phosphorus_export_kg_ha_proxy": p_export,
        "annual_N_balance_kg_ha": n_balance,
        "annual_P_balance_kg_ha": p_balance,
        "pH_pressure": pH_pressure(row["pH"]),
        "salinity_pressure": salinity_pressure(row["electrical_conductivity_dS_m"]),
        "contaminant_pressure": contaminant_pressure(row),
        "soil_land_system_pressure_index": pressure,
        "attention_flag": attention_flag,
    }


def summarize_by_land_use(indicators: list[dict]) -> list[dict]:
    """Summarize indicators by land use."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["land_use"], []).append(row)

    summaries: list[dict] = []

    for land_use, records in sorted(grouped.items()):
        summaries.append(
            {
                "land_use": land_use,
                "n": len(records),
                "mean_pH": mean(row["pH"] for row in records),
                "mean_soc_percent": mean(row["soc_percent"] for row in records),
                "mean_soc_stock_Mg_ha": mean(row["soc_stock_Mg_ha"] for row in records),
                "mean_base_saturation_percent": mean(row["base_saturation_percent"] for row in records),
                "mean_nitrate_leaching_vulnerability": mean(row["nitrate_leaching_vulnerability"] for row in records),
                "mean_phosphorus_export_kg_ha_proxy": mean(row["phosphorus_export_kg_ha_proxy"] for row in records),
                "mean_soil_land_system_pressure_index": mean(row["soil_land_system_pressure_index"] for row in records),
            }
        )

    return summaries


def build_soil_carbon_scenario(base_row: dict) -> list[dict]:
    """
    Build a simple soil carbon scenario.

    Three scenarios are included:
    - baseline
    - restoration
    - degradation

    This is educational and does not represent verified carbon accounting.
    """
    rows: list[dict] = []

    scenarios = {
        "baseline": {"target_soc": base_row["soc_percent"], "rate": 0.02},
        "restoration": {"target_soc": 5.0, "rate": 0.045},
        "degradation": {"target_soc": 0.8, "rate": 0.035},
    }

    for scenario, params in scenarios.items():
        soc = base_row["soc_percent"]

        for year in range(0, 41):
            target = params["target_soc"]
            rate = params["rate"]
            soc = soc + rate * (target - soc)

            rows.append(
                {
                    "scenario": scenario,
                    "year": year,
                    "modeled_soc_percent": soc,
                    "modeled_soc_stock_Mg_ha": soc_stock_mg_ha(
                        soc,
                        base_row["bulk_density_g_cm3"],
                        base_row["depth_cm"],
                    ),
                }
            )

    return rows


def build_nitrogen_balance_scenario(base_row: dict) -> list[dict]:
    """
    Build nitrogen balance scenarios for annual input management.

    This is a simplified mass-balance teaching model.
    """
    rows: list[dict] = []

    input_multipliers = [0.75, 1.0, 1.25, 1.50]
    leaching_factors = [0.10, 0.20, 0.35]

    for multiplier in input_multipliers:
        for leaching_fraction in leaching_factors:
            n_input = base_row["annual_N_input_kg_ha"] * multiplier
            harvest_removal = base_row["annual_N_removal_kg_ha"]
            leaching_loss = n_input * leaching_fraction
            gaseous_loss = n_input * 0.08
            net_n = n_input - harvest_removal - leaching_loss - gaseous_loss

            rows.append(
                {
                    "input_multiplier": multiplier,
                    "leaching_fraction": leaching_fraction,
                    "N_input_kg_ha": n_input,
                    "harvest_removal_kg_ha": harvest_removal,
                    "leaching_loss_kg_ha": leaching_loss,
                    "gaseous_loss_kg_ha": gaseous_loss,
                    "net_N_balance_kg_ha": net_n,
                }
            )

    return rows


def build_phosphorus_export_scenario(base_row: dict) -> list[dict]:
    """Build phosphorus export scenarios across erosion-control levels."""
    rows: list[dict] = []

    for erosion_reduction_percent in range(0, 91, 10):
        reduced_erosion = base_row["erosion_t_ha"] * (1.0 - erosion_reduction_percent / 100.0)
        p_export = phosphorus_export_proxy(reduced_erosion, base_row["sediment_p_mg_kg"])

        rows.append(
            {
                "erosion_reduction_percent": erosion_reduction_percent,
                "modeled_erosion_t_ha": reduced_erosion,
                "modeled_phosphorus_export_kg_ha": p_export,
            }
        )

    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write rows to CSV using union fieldnames."""
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(indicators: list[dict], summaries: list[dict]) -> None:
    """Write an advanced Markdown report."""
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    high_attention = [
        row for row in indicators
        if row["attention_flag"] == "high_attention"
    ]

    moderate_attention = [
        row for row in indicators
        if row["attention_flag"] == "moderate_attention"
    ]

    high_p_export = [
        row for row in indicators
        if row["phosphorus_export_kg_ha_proxy"] >= 4.0
    ]

    high_contaminant = [
        row for row in indicators
        if row["contaminant_pressure"] >= 0.80
    ]

    lines = [
        "# Advanced Soil Chemistry Report",
        "",
        "This report summarizes synthetic soil chemistry indicators for the article **Soil Chemistry, Nutrient Cycles, and Land Systems**.",
        "",
        f"Total records: {len(indicators)}",
        f"High attention records: {len(high_attention)}",
        f"Moderate attention records: {len(moderate_attention)}",
        f"High phosphorus export proxy records: {len(high_p_export)}",
        f"High contaminant pressure records: {len(high_contaminant)}",
        "",
        "## High attention records",
        "",
    ]

    for row in high_attention:
        lines.append(
            f"- {row['site']} ({row['land_use']}): "
            f"pressure index={row['soil_land_system_pressure_index']:.3f}, "
            f"pH={row['pH']:.2f}, "
            f"nitrate vulnerability={row['nitrate_leaching_vulnerability']:.3f}, "
            f"P export={row['phosphorus_export_kg_ha_proxy']:.2f} kg/ha, "
            f"contaminant pressure={row['contaminant_pressure']:.3f}"
        )

    lines.extend(["", "## Land-use summaries", ""])

    for row in summaries:
        lines.append(
            f"- {row['land_use']}: "
            f"mean SOC stock={row['mean_soc_stock_Mg_ha']:.2f} Mg/ha, "
            f"mean base saturation={row['mean_base_saturation_percent']:.1f}%, "
            f"mean pressure index={row['mean_soil_land_system_pressure_index']:.3f}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not agronomic recommendations, soil-carbon credit estimates, contamination assessments, public-health advisories, legal evidence, land valuations, or regulatory determinations.",
        ]
    )

    (OUT_REPORTS / "advanced_soil_chemistry_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(
    indicators: list[dict],
    summaries: list[dict],
    carbon_series: list[dict],
    nitrogen_series: list[dict],
    phosphorus_series: list[dict],
) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "soil-chemistry-nutrient-cycles-land-systems",
        "title": "Soil Chemistry, Nutrient Cycles, and Land Systems",
        "advanced_layer": True,
        "synthetic_records": len(indicators),
        "summary_groups": len(summaries),
        "carbon_scenario_rows": len(carbon_series),
        "nitrogen_scenario_rows": len(nitrogen_series),
        "phosphorus_scenario_rows": len(phosphorus_series),
        "outputs": [
            "advanced/outputs/tables/advanced_soil_chemistry_indicators.csv",
            "advanced/outputs/tables/advanced_land_use_summary.csv",
            "advanced/outputs/tables/advanced_soil_carbon_scenarios.csv",
            "advanced/outputs/tables/advanced_nitrogen_balance_scenarios.csv",
            "advanced/outputs/tables/advanced_phosphorus_export_scenarios.csv",
            "advanced/outputs/reports/advanced_soil_chemistry_report.md",
        ],
        "responsible_use": "Synthetic educational soil chemistry workflow only; not for agronomic, carbon-credit, contamination, public-health, legal, valuation, or regulatory decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced soil chemistry workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_land_use(indicators)

    carbon_series = build_soil_carbon_scenario(rows[0])
    nitrogen_series = build_nitrogen_balance_scenario(rows[1])
    phosphorus_series = build_phosphorus_export_scenario(rows[1])

    write_csv(OUT_TABLES / "advanced_soil_chemistry_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_land_use_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_soil_carbon_scenarios.csv", carbon_series)
    write_csv(OUT_TABLES / "advanced_nitrogen_balance_scenarios.csv", nitrogen_series)
    write_csv(OUT_TABLES / "advanced_phosphorus_export_scenarios.csv", phosphorus_series)

    write_report(indicators, summaries)
    write_manifest(indicators, summaries, carbon_series, nitrogen_series, phosphorus_series)

    print("Advanced soil chemistry workflow complete.")
    print(f"Records: {len(indicators)}")
    print(f"Land-use summaries: {len(summaries)}")
    print(f"Soil carbon scenario rows: {len(carbon_series)}")
    print(f"Nitrogen scenario rows: {len(nitrogen_series)}")
    print(f"Phosphorus scenario rows: {len(phosphorus_series)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
