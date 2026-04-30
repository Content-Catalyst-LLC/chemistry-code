#!/usr/bin/env python3
"""
Advanced ocean carbonate chemistry workflow.

Article:
Ocean Chemistry and the Carbonate System

This script uses synthetic ocean carbonate monitoring data to calculate:

- carbonate species fractions
- CO2*, bicarbonate, and carbonate ion estimates
- aragonite and calcite saturation states
- air-sea CO2 flux proxy
- alkalinity-DIC buffer ratio
- Revelle-factor intuition proxy
- acidification pressure index
- DIC perturbation sensitivity series
- grouped summaries by water type

This is educational scaffolding only. It is not a replacement for CO2SYS,
PyCO2SYS, seacarb, AquaEnv, OCADS workflows, certified measurements, or
research-grade carbonate chemistry.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "ocean_carbonate_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

# Simplified constants for educational carbonate chemistry only.
# Research-grade work must use temperature-, salinity-, pressure-, nutrient-,
# and pH-scale-dependent constants.
K1 = 10 ** -6.0
K2 = 10 ** -9.1
KSP_ARAGONITE = 6.5e-7
KSP_CALCITE = 4.4e-7


NUMERIC_FIELDS = {
    "depth_m",
    "temperature_c",
    "salinity",
    "pH_total_scale",
    "DIC_umol_kg",
    "total_alkalinity_umol_kg",
    "pCO2_water_uatm",
    "pCO2_air_uatm",
    "calcium_mmol_kg",
    "oxygen_umol_kg",
    "nitrate_umol_kg",
    "phosphate_umol_kg",
    "silicate_umol_kg",
    "wind_speed_m_s",
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
    """Load synthetic carbonate monitoring records."""
    rows: list[dict] = []

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(key, value) for key, value in row.items()})

    return rows


def carbonate_fractions(pH: float) -> dict:
    """
    Calculate simplified carbonate alpha fractions.

    alpha0 = fraction as CO2*
    alpha1 = fraction as HCO3-
    alpha2 = fraction as CO3--

    This uses fixed educational constants.
    """
    hydrogen = 10 ** (-pH)
    denominator = hydrogen**2 + K1 * hydrogen + K1 * K2

    return {
        "alpha_CO2_star": hydrogen**2 / denominator,
        "alpha_HCO3": K1 * hydrogen / denominator,
        "alpha_CO3": K1 * K2 / denominator,
    }


def carbonate_species_umol_kg(pH: float, dic_umol_kg: float) -> dict:
    """Estimate carbonate-system species from DIC and pH."""
    fractions = carbonate_fractions(pH)

    return {
        **fractions,
        "CO2_star_umol_kg": fractions["alpha_CO2_star"] * dic_umol_kg,
        "bicarbonate_umol_kg": fractions["alpha_HCO3"] * dic_umol_kg,
        "carbonate_umol_kg": fractions["alpha_CO3"] * dic_umol_kg,
    }


def saturation_state(calcium_mmol_kg: float, carbonate_umol_kg: float, ksp: float) -> float:
    """Calculate simplified calcium carbonate saturation state."""
    calcium_mol_kg = calcium_mmol_kg * 1e-3
    carbonate_mol_kg = carbonate_umol_kg * 1e-6
    return calcium_mol_kg * carbonate_mol_kg / ksp


def gas_transfer_velocity_proxy(wind_speed_m_s: float) -> float:
    """
    Educational gas-transfer proxy.

    This is not a calibrated gas-transfer parameterization.
    It gives a wind-scaled coefficient for comparing synthetic records.
    """
    return 0.251 * wind_speed_m_s**2


def air_sea_co2_flux_proxy(
    pco2_water_uatm: float,
    pco2_air_uatm: float,
    wind_speed_m_s: float,
) -> float:
    """
    Simplified air-sea CO2 flux proxy.

    Positive values mean ocean-to-atmosphere outgassing potential
    under this sign convention.
    """
    delta_pco2 = pco2_water_uatm - pco2_air_uatm
    return gas_transfer_velocity_proxy(wind_speed_m_s) * delta_pco2


def revelle_factor_intuition_proxy(
    pH: float,
    dic_umol_kg: float,
    total_alkalinity_umol_kg: float,
) -> float:
    """
    Conceptual Revelle-factor proxy.

    This is not a formal Revelle-factor calculation. It increases when
    carbonate buffering is weaker, pH is lower, or DIC is high relative to TA.
    """
    buffer_ratio = total_alkalinity_umol_kg / dic_umol_kg
    pH_component = max(0.0, 8.15 - pH) * 8.0
    buffer_component = max(0.0, 1.15 - buffer_ratio) * 12.0
    return 8.0 + pH_component + buffer_component


def acidification_pressure_index(row: dict, omega_aragonite: float, flux_proxy: float) -> float:
    """
    Build a composite educational acidification-pressure index.

    Components:
    - lower pH
    - lower aragonite saturation
    - large air-sea CO2 disequilibrium
    - lower alkalinity/DIC buffer ratio
    - lower data quality
    """
    pH_pressure = clamp((8.15 - row["pH_total_scale"]) / 0.65)
    saturation_pressure = clamp((2.5 - omega_aragonite) / 2.5)
    flux_pressure = clamp(abs(flux_proxy) / 10000.0)
    buffer_ratio = row["total_alkalinity_umol_kg"] / row["DIC_umol_kg"]
    buffer_pressure = clamp((1.15 - buffer_ratio) / 0.25)
    qc_pressure = 1.0 - row["qc_score"]

    return clamp(
        0.32 * pH_pressure
        + 0.28 * saturation_pressure
        + 0.18 * flux_pressure
        + 0.14 * buffer_pressure
        + 0.08 * qc_pressure
    )


def enrich_row(row: dict) -> dict:
    """Add carbonate-system indicators to one monitoring row."""
    species = carbonate_species_umol_kg(
        pH=row["pH_total_scale"],
        dic_umol_kg=row["DIC_umol_kg"],
    )

    omega_aragonite = saturation_state(
        calcium_mmol_kg=row["calcium_mmol_kg"],
        carbonate_umol_kg=species["carbonate_umol_kg"],
        ksp=KSP_ARAGONITE,
    )

    omega_calcite = saturation_state(
        calcium_mmol_kg=row["calcium_mmol_kg"],
        carbonate_umol_kg=species["carbonate_umol_kg"],
        ksp=KSP_CALCITE,
    )

    flux_proxy = air_sea_co2_flux_proxy(
        pco2_water_uatm=row["pCO2_water_uatm"],
        pco2_air_uatm=row["pCO2_air_uatm"],
        wind_speed_m_s=row["wind_speed_m_s"],
    )

    buffer_ratio = row["total_alkalinity_umol_kg"] / row["DIC_umol_kg"]
    revelle_proxy = revelle_factor_intuition_proxy(
        pH=row["pH_total_scale"],
        dic_umol_kg=row["DIC_umol_kg"],
        total_alkalinity_umol_kg=row["total_alkalinity_umol_kg"],
    )

    pressure = acidification_pressure_index(row, omega_aragonite, flux_proxy)

    if omega_aragonite < 1.0:
        saturation_flag = "undersaturated_attention"
    elif omega_aragonite < 2.0:
        saturation_flag = "low_saturation_attention"
    else:
        saturation_flag = "higher_saturation_screen"

    return {
        **row,
        **species,
        "omega_aragonite_simplified": omega_aragonite,
        "omega_calcite_simplified": omega_calcite,
        "alkalinity_DIC_buffer_ratio": buffer_ratio,
        "air_sea_CO2_flux_proxy": flux_proxy,
        "revelle_factor_intuition_proxy": revelle_proxy,
        "acidification_pressure_index": pressure,
        "saturation_flag": saturation_flag,
        "attention_flag": "high_attention" if pressure >= 0.55 else "monitor",
    }


def build_sensitivity_series(base_row: dict) -> list[dict]:
    """
    Build a synthetic DIC perturbation series.

    This shows how increasing DIC can lower pH, reduce carbonate ion,
    and reduce aragonite saturation in a simplified educational model.
    """
    rows: list[dict] = []

    for added_dic in range(0, 421, 20):
        modeled_dic = base_row["DIC_umol_kg"] + added_dic

        # Educational pH response approximation only.
        modeled_pH = base_row["pH_total_scale"] - 0.00095 * added_dic

        species = carbonate_species_umol_kg(modeled_pH, modeled_dic)
        omega = saturation_state(
            calcium_mmol_kg=base_row["calcium_mmol_kg"],
            carbonate_umol_kg=species["carbonate_umol_kg"],
            ksp=KSP_ARAGONITE,
        )

        rows.append(
            {
                "station": base_row["station"],
                "added_DIC_umol_kg": added_dic,
                "modeled_DIC_umol_kg": modeled_dic,
                "modeled_pH_total_scale": modeled_pH,
                "modeled_CO2_star_umol_kg": species["CO2_star_umol_kg"],
                "modeled_bicarbonate_umol_kg": species["bicarbonate_umol_kg"],
                "modeled_carbonate_umol_kg": species["carbonate_umol_kg"],
                "modeled_omega_aragonite": omega,
            }
        )

    return rows


def summarize_by_water_type(indicators: list[dict]) -> list[dict]:
    """Summarize key indicators by water type."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["water_type"], []).append(row)

    summaries: list[dict] = []

    for water_type, records in sorted(grouped.items()):
        summaries.append(
            {
                "water_type": water_type,
                "n": len(records),
                "mean_pH_total_scale": mean(row["pH_total_scale"] for row in records),
                "mean_DIC_umol_kg": mean(row["DIC_umol_kg"] for row in records),
                "mean_total_alkalinity_umol_kg": mean(row["total_alkalinity_umol_kg"] for row in records),
                "mean_carbonate_umol_kg": mean(row["carbonate_umol_kg"] for row in records),
                "mean_omega_aragonite_simplified": mean(row["omega_aragonite_simplified"] for row in records),
                "mean_air_sea_CO2_flux_proxy": mean(row["air_sea_CO2_flux_proxy"] for row in records),
                "mean_acidification_pressure_index": mean(row["acidification_pressure_index"] for row in records),
            }
        )

    return summaries


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write rows to CSV."""
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(indicators: list[dict], summaries: list[dict]) -> None:
    """Write an advanced Markdown report."""
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    low_saturation = [
        row for row in indicators
        if row["saturation_flag"] in {"undersaturated_attention", "low_saturation_attention"}
    ]

    high_attention = [
        row for row in indicators
        if row["attention_flag"] == "high_attention"
    ]

    lines = [
        "# Advanced Ocean Carbonate Chemistry Report",
        "",
        "This report summarizes synthetic carbonate-system indicators for the article **Ocean Chemistry and the Carbonate System**.",
        "",
        f"Total records: {len(indicators)}",
        f"Low saturation records: {len(low_saturation)}",
        f"High acidification-pressure records: {len(high_attention)}",
        "",
        "## Low saturation records",
        "",
    ]

    for row in low_saturation:
        lines.append(
            f"- {row['station']} ({row['water_type']}): "
            f"pH={row['pH_total_scale']:.2f}, "
            f"carbonate={row['carbonate_umol_kg']:.2f} umol/kg, "
            f"Omega_aragonite={row['omega_aragonite_simplified']:.2f}, "
            f"flag={row['saturation_flag']}"
        )

    lines.extend(["", "## Water-type summaries", ""])

    for row in summaries:
        lines.append(
            f"- {row['water_type']}: "
            f"mean pH={row['mean_pH_total_scale']:.2f}, "
            f"mean Omega_aragonite={row['mean_omega_aragonite_simplified']:.2f}, "
            f"mean pressure index={row['mean_acidification_pressure_index']:.3f}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not research-grade carbonate-system outputs, regulatory findings, hatchery advisories, operational forecasts, climate-attribution results, or legal evidence.",
        ]
    )

    (OUT_REPORTS / "advanced_ocean_carbonate_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(indicators: list[dict], summaries: list[dict], sensitivity: list[dict]) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "ocean-chemistry-carbonate-system",
        "title": "Ocean Chemistry and the Carbonate System",
        "advanced_layer": True,
        "synthetic_records": len(indicators),
        "summary_groups": len(summaries),
        "sensitivity_rows": len(sensitivity),
        "outputs": [
            "advanced/outputs/tables/advanced_ocean_carbonate_indicators.csv",
            "advanced/outputs/tables/advanced_ocean_water_type_summary.csv",
            "advanced/outputs/tables/advanced_dic_sensitivity_series.csv",
            "advanced/outputs/reports/advanced_ocean_carbonate_report.md",
        ],
        "responsible_use": "Synthetic educational carbonate-system workflow only; not for research-grade, regulatory, operational, legal, or climate-attribution decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_water_type(indicators)
    sensitivity = build_sensitivity_series(rows[0])

    write_csv(OUT_TABLES / "advanced_ocean_carbonate_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_ocean_water_type_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_dic_sensitivity_series.csv", sensitivity)

    write_report(indicators, summaries)
    write_manifest(indicators, summaries, sensitivity)

    print("Advanced ocean carbonate workflow complete.")
    print(f"Records: {len(indicators)}")
    print(f"Water-type summaries: {len(summaries)}")
    print(f"Sensitivity rows: {len(sensitivity)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
