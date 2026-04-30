#!/usr/bin/env python3
"""
Advanced environmental chemistry workflow.

Article:
Environmental Chemistry and the Chemical Conditions of Habitability

This script uses synthetic environmental chemistry monitoring data to calculate:

- benchmark exceedance ratios
- load estimates where flow is available
- organic-carbon partitioning via Kd = Koc * foc
- retardation factor proxies
- Henry-law air-water tendency proxies
- first-order decay and persistence
- pH stress, redox stress, oxygen stress, nutrient pressure
- contaminant pressure and exposure-pathway pressure
- receptor sensitivity and QA-weighted evidence pressure
- composite chemical habitability pressure index
- Monte Carlo exceedance probabilities
- decay scenario series
- leaching/retardation scenario series
- multimedia partitioning scenario series
- grouped summaries by compartment

This is educational scaffolding only. It is not a regulatory compliance tool,
public-health advisory, environmental forensic report, site-remediation design,
legal analysis, ecological risk assessment, drinking-water determination,
hazardous-waste determination, or operational monitoring system.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "environmental_chemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "concentration",
    "benchmark",
    "pH",
    "temperature_c",
    "organic_carbon_fraction",
    "koc_L_kg",
    "henry_atm_m3_mol",
    "half_life_days",
    "flow_L_s",
    "water_depth_m",
    "bulk_density_g_cm3",
    "porosity_fraction",
    "exposure_weight",
    "receptor_sensitivity",
    "redox_Eh_mV",
    "dissolved_oxygen_mg_L",
    "nitrate_mg_L",
    "phosphate_mg_L",
    "sulfate_mg_L",
    "chloride_mg_L",
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
    """Load synthetic environmental chemistry records."""
    rows: list[dict] = []

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(key, value) for key, value in row.items()})

    return rows


def benchmark_ratio(concentration: float, benchmark: float) -> float:
    """Calculate concentration / benchmark."""
    if benchmark <= 0:
        return 0.0
    return concentration / benchmark


def concentration_load_kg_day(concentration: float, unit: str, flow_L_s: float) -> float | None:
    """
    Convert concentration and flow to approximate daily load.

    mg/L:
        kg/day = concentration_mg_L * flow_L_s * 0.0864

    ug/L:
        kg/day = concentration_ug_L * flow_L_s * 0.0000864
    """
    if flow_L_s <= 0:
        return None

    if unit == "mg/L":
        return concentration * flow_L_s * 0.0864

    if unit == "ug/L":
        return concentration * flow_L_s * 0.0000864

    return None


def kd_L_kg(koc_L_kg: float, organic_carbon_fraction: float) -> float:
    """
    Soil/sediment-water distribution coefficient proxy.

    Kd = Koc * foc
    """
    return koc_L_kg * organic_carbon_fraction


def retardation_factor(kd: float, bulk_density_g_cm3: float, porosity_fraction: float) -> float:
    """
    Retardation factor proxy.

    R = 1 + (rho_b * Kd) / n

    Here rho_b is approximated in kg/L using g/cm3 equivalence.
    """
    porosity = max(porosity_fraction, 0.01)
    return 1.0 + (bulk_density_g_cm3 * kd) / porosity


def henry_air_water_tendency(henry_atm_m3_mol: float) -> float:
    """
    Simplified volatilization tendency.

    This bounded index increases with Henry's law constant.
    It is not a full dimensionless Henry conversion.
    """
    return clamp(math.log1p(max(henry_atm_m3_mol, 0.0) * 1000.0) / math.log(20.0))


def first_order_decay_constant_per_day(half_life_days: float) -> float:
    """Convert half-life to first-order decay constant."""
    if half_life_days <= 0:
        return 0.0
    return math.log(2.0) / half_life_days


def persistence_factor(half_life_days: float) -> float:
    """Bounded persistence proxy."""
    return half_life_days / (half_life_days + 90.0)


def pH_stress_index(pH: float) -> float:
    """Simplified pH stress outside a broad habitability-supporting range."""
    if pH < 6.0:
        return clamp((6.0 - pH) / 2.5)
    if pH > 8.5:
        return clamp((pH - 8.5) / 2.5)
    return 0.0


def redox_stress_index(redox_Eh_mV: float, compartment: str) -> float:
    """
    Simplified redox stress.

    Very reducing conditions may increase mobility of some metals and metalloids.
    Strongly oxidizing conditions may increase oxidative stress or secondary chemistry.
    """
    if compartment in {"groundwater", "sediment", "wetland_water"}:
        reducing_component = clamp((100.0 - redox_Eh_mV) / 250.0)
        oxidizing_component = clamp((redox_Eh_mV - 500.0) / 250.0)
        return max(reducing_component, oxidizing_component)

    return clamp(abs(redox_Eh_mV - 300.0) / 500.0)


def oxygen_stress_index(dissolved_oxygen_mg_L: float, compartment: str) -> float:
    """Simplified oxygen stress for aquatic compartments."""
    if compartment in {"surface_water", "groundwater", "stormwater", "wetland_water"}:
        return clamp((5.0 - dissolved_oxygen_mg_L) / 5.0)
    return 0.0


def nutrient_pressure_index(nitrate_mg_L: float, phosphate_mg_L: float) -> float:
    """Simplified nutrient pressure index."""
    nitrate_component = clamp(nitrate_mg_L / 10.0)
    phosphate_component = clamp(phosphate_mg_L / 0.20)
    return clamp(0.50 * nitrate_component + 0.50 * phosphate_component)


def ionic_pressure_index(sulfate_mg_L: float, chloride_mg_L: float) -> float:
    """Simplified ionic/salinity pressure index."""
    sulfate_component = clamp((sulfate_mg_L - 250.0) / 750.0)
    chloride_component = clamp((chloride_mg_L - 100.0) / 500.0)
    return max(sulfate_component, chloride_component)


def contaminant_pressure_index(row: dict) -> float:
    """
    Contaminant pressure depends on benchmark ratio, persistence,
    mobility/retardation, volatility, and analyte class.
    """
    ratio_component = clamp(math.log1p(benchmark_ratio(row["concentration"], row["benchmark"])) / math.log(5.0))
    persistence_component = persistence_factor(row["half_life_days"])
    kd_value = kd_L_kg(row["koc_L_kg"], row["organic_carbon_fraction"])
    retardation = retardation_factor(kd_value, row["bulk_density_g_cm3"], row["porosity_fraction"])

    mobility_component = 1.0 / math.sqrt(max(retardation, 1.0))
    volatility_component = henry_air_water_tendency(row["henry_atm_m3_mol"])

    class_weight = {
        "nutrient": 0.65,
        "metal": 0.90,
        "metalloid": 0.95,
        "pah": 0.85,
        "chlorinated_solvent": 0.95,
        "secondary_pollutant": 0.80,
        "cyanotoxin": 1.00,
    }.get(row["analyte_class"], 0.75)

    return clamp(
        class_weight
        * (
            0.35 * ratio_component
            + 0.20 * persistence_component
            + 0.18 * mobility_component
            + 0.12 * volatility_component
            + 0.15 * row["exposure_weight"]
        )
    )


def chemical_habitability_pressure_index(row: dict) -> float:
    """
    Composite chemical habitability pressure index.

    Components:
    - contaminant pressure
    - nutrient pressure
    - pH stress
    - redox stress
    - oxygen stress
    - ionic pressure
    - receptor sensitivity
    - QA penalty
    """
    contaminant_pressure = contaminant_pressure_index(row)
    nutrient_pressure = nutrient_pressure_index(row["nitrate_mg_L"], row["phosphate_mg_L"])
    ph_pressure = pH_stress_index(row["pH"])
    redox_pressure = redox_stress_index(row["redox_Eh_mV"], row["compartment"])
    oxygen_pressure = oxygen_stress_index(row["dissolved_oxygen_mg_L"], row["compartment"])
    ionic_pressure = ionic_pressure_index(row["sulfate_mg_L"], row["chloride_mg_L"])
    qc_penalty = 1.0 - row["qc_score"]

    return clamp(
        0.30 * contaminant_pressure
        + 0.16 * nutrient_pressure
        + 0.12 * ph_pressure
        + 0.12 * redox_pressure
        + 0.10 * oxygen_pressure
        + 0.08 * ionic_pressure
        + 0.08 * row["receptor_sensitivity"]
        + 0.04 * qc_penalty
    )


def monte_carlo_exceedance_probability(
    concentration: float,
    benchmark: float,
    qc_score: float,
    draws: int = 1000,
    seed: int = 42,
) -> dict:
    """
    Estimate exceedance probability using a simple lognormal uncertainty model.

    Lower QC score increases uncertainty. This is a teaching model, not a
    validated measurement-error model.
    """
    rng = random.Random(seed)
    uncertainty_sigma = 0.05 + (1.0 - qc_score) * 0.35

    exceedances = 0
    values = []

    for _ in range(draws):
        multiplier = rng.lognormvariate(mu=0.0, sigma=uncertainty_sigma)
        simulated = concentration * multiplier
        values.append(simulated)
        if simulated > benchmark:
            exceedances += 1

    values.sort()

    def percentile(p: float) -> float:
        index = int(round((p / 100.0) * (len(values) - 1)))
        return values[index]

    return {
        "exceedance_probability": exceedances / draws,
        "mc_p05": percentile(5),
        "mc_p50": percentile(50),
        "mc_p95": percentile(95),
        "draws": draws,
        "uncertainty_sigma": uncertainty_sigma,
    }


def enrich_row(row: dict) -> dict:
    """Add advanced environmental chemistry indicators to one row."""
    ratio = benchmark_ratio(row["concentration"], row["benchmark"])
    load = concentration_load_kg_day(row["concentration"], row["unit"], row["flow_L_s"])
    kd_value = kd_L_kg(row["koc_L_kg"], row["organic_carbon_fraction"])
    retardation = retardation_factor(kd_value, row["bulk_density_g_cm3"], row["porosity_fraction"])
    decay_constant = first_order_decay_constant_per_day(row["half_life_days"])
    mc = monte_carlo_exceedance_probability(
        row["concentration"],
        row["benchmark"],
        row["qc_score"],
        draws=1000,
        seed=abs(hash(row["sample_id"])) % 100000,
    )

    contaminant_pressure = contaminant_pressure_index(row)
    habitability_pressure = chemical_habitability_pressure_index(row)

    if habitability_pressure >= 0.65:
        attention_flag = "high_attention"
    elif habitability_pressure >= 0.45:
        attention_flag = "moderate_attention"
    else:
        attention_flag = "monitor"

    return {
        **row,
        "benchmark_ratio": ratio,
        "load_kg_day": load,
        "Kd_L_kg": kd_value,
        "retardation_factor_proxy": retardation,
        "mobility_factor_proxy": 1.0 / math.sqrt(max(retardation, 1.0)),
        "henry_air_water_tendency": henry_air_water_tendency(row["henry_atm_m3_mol"]),
        "decay_constant_per_day": decay_constant,
        "persistence_factor": persistence_factor(row["half_life_days"]),
        "pH_stress_index": pH_stress_index(row["pH"]),
        "redox_stress_index": redox_stress_index(row["redox_Eh_mV"], row["compartment"]),
        "oxygen_stress_index": oxygen_stress_index(row["dissolved_oxygen_mg_L"], row["compartment"]),
        "nutrient_pressure_index": nutrient_pressure_index(row["nitrate_mg_L"], row["phosphate_mg_L"]),
        "ionic_pressure_index": ionic_pressure_index(row["sulfate_mg_L"], row["chloride_mg_L"]),
        "contaminant_pressure_index": contaminant_pressure,
        "chemical_habitability_pressure_index": habitability_pressure,
        "evidence_weighted_habitability_pressure": habitability_pressure * row["qc_score"],
        "monte_carlo_exceedance_probability": mc["exceedance_probability"],
        "mc_concentration_p05": mc["mc_p05"],
        "mc_concentration_p50": mc["mc_p50"],
        "mc_concentration_p95": mc["mc_p95"],
        "mc_uncertainty_sigma": mc["uncertainty_sigma"],
        "attention_flag": attention_flag,
    }


def summarize_by_compartment(indicators: list[dict]) -> list[dict]:
    """Summarize indicators by environmental compartment."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["compartment"], []).append(row)

    summaries: list[dict] = []

    for compartment, records in sorted(grouped.items()):
        loads = [row["load_kg_day"] for row in records if row["load_kg_day"] is not None]

        summaries.append(
            {
                "compartment": compartment,
                "n": len(records),
                "mean_benchmark_ratio": mean(row["benchmark_ratio"] for row in records),
                "mean_Kd_L_kg": mean(row["Kd_L_kg"] for row in records),
                "mean_retardation_factor_proxy": mean(row["retardation_factor_proxy"] for row in records),
                "mean_persistence_factor": mean(row["persistence_factor"] for row in records),
                "mean_nutrient_pressure_index": mean(row["nutrient_pressure_index"] for row in records),
                "mean_contaminant_pressure_index": mean(row["contaminant_pressure_index"] for row in records),
                "mean_chemical_habitability_pressure_index": mean(row["chemical_habitability_pressure_index"] for row in records),
                "mean_monte_carlo_exceedance_probability": mean(row["monte_carlo_exceedance_probability"] for row in records),
                "total_load_kg_day": sum(loads) if loads else None,
            }
        )

    return summaries


def build_decay_scenario(base_row: dict) -> list[dict]:
    """Build a first-order decay scenario for one analyte."""
    rows: list[dict] = []

    k = first_order_decay_constant_per_day(base_row["half_life_days"])
    initial = base_row["concentration"]

    for day in range(0, 731, 30):
        concentration = initial * math.exp(-k * day)

        rows.append(
            {
                "scenario": "first_order_decay",
                "site": base_row["site"],
                "analyte": base_row["analyte"],
                "day": day,
                "modeled_concentration": concentration,
                "unit": base_row["unit"],
                "fraction_remaining": concentration / initial if initial else 0.0,
            }
        )

    return rows


def build_leaching_retardation_scenario(base_row: dict) -> list[dict]:
    """
    Build a retardation/leaching scenario across organic carbon and porosity.

    This is a proxy, not a transport model.
    """
    rows: list[dict] = []

    foc_values = [0.001, 0.005, 0.010, 0.020, 0.050]
    porosity_values = [0.25, 0.35, 0.45, 0.60]

    for foc in foc_values:
        for porosity in porosity_values:
            kd_value = kd_L_kg(base_row["koc_L_kg"], foc)
            retardation = retardation_factor(
                kd_value,
                base_row["bulk_density_g_cm3"],
                porosity,
            )

            rows.append(
                {
                    "scenario": "leaching_retardation",
                    "analyte": base_row["analyte"],
                    "organic_carbon_fraction": foc,
                    "porosity_fraction": porosity,
                    "Kd_L_kg": kd_value,
                    "retardation_factor_proxy": retardation,
                    "mobility_factor_proxy": 1.0 / math.sqrt(max(retardation, 1.0)),
                }
            )

    return rows


def build_multimedia_partition_scenario(base_row: dict) -> list[dict]:
    """
    Build a simplified multimedia partitioning scenario.

    This is an interpretable teaching proxy using relative affinities, not a
    fugacity model.
    """
    rows: list[dict] = []

    foc_values = [0.001, 0.010, 0.030, 0.060]
    henry_multipliers = [0.1, 1.0, 10.0]

    for foc in foc_values:
        for h_multiplier in henry_multipliers:
            kd_value = kd_L_kg(base_row["koc_L_kg"], foc)
            air_affinity = henry_air_water_tendency(base_row["henry_atm_m3_mol"] * h_multiplier)
            solid_affinity = clamp(math.log1p(kd_value) / math.log(1000.0))
            water_affinity = max(1.0 - 0.5 * air_affinity - 0.5 * solid_affinity, 0.0)

            total = air_affinity + solid_affinity + water_affinity
            if total <= 0:
                total = 1.0

            rows.append(
                {
                    "scenario": "multimedia_partition_proxy",
                    "analyte": base_row["analyte"],
                    "organic_carbon_fraction": foc,
                    "henry_multiplier": h_multiplier,
                    "relative_air_fraction_proxy": air_affinity / total,
                    "relative_solid_fraction_proxy": solid_affinity / total,
                    "relative_water_fraction_proxy": water_affinity / total,
                }
            )

    return rows


def build_exposure_pathway_scenario(base_row: dict) -> list[dict]:
    """Build exposure pathway scenario across receptor sensitivity and exposure weight."""
    rows: list[dict] = []

    exposure_values = [0.25, 0.50, 0.75, 1.00]
    sensitivity_values = [0.25, 0.50, 0.75, 1.00]

    for exposure in exposure_values:
        for sensitivity in sensitivity_values:
            modeled = dict(base_row)
            modeled["exposure_weight"] = exposure
            modeled["receptor_sensitivity"] = sensitivity

            rows.append(
                {
                    "scenario": "exposure_pathway_sensitivity",
                    "analyte": base_row["analyte"],
                    "exposure_weight": exposure,
                    "receptor_sensitivity": sensitivity,
                    "chemical_habitability_pressure_index": chemical_habitability_pressure_index(modeled),
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

    benchmark_exceedances = [
        row for row in indicators
        if row["benchmark_ratio"] > 1.0
    ]

    high_mc_exceedance = [
        row for row in indicators
        if row["monte_carlo_exceedance_probability"] >= 0.80
    ]

    lines = [
        "# Advanced Environmental Chemistry Report",
        "",
        "This report summarizes synthetic environmental chemistry indicators for the article **Environmental Chemistry and the Chemical Conditions of Habitability**.",
        "",
        f"Total records: {len(indicators)}",
        f"Benchmark exceedances: {len(benchmark_exceedances)}",
        f"High Monte Carlo exceedance-probability records: {len(high_mc_exceedance)}",
        f"High attention records: {len(high_attention)}",
        f"Moderate attention records: {len(moderate_attention)}",
        "",
        "## High attention records",
        "",
    ]

    for row in high_attention:
        load_text = "NA" if row["load_kg_day"] is None else f"{row['load_kg_day']:.3f} kg/day"
        lines.append(
            f"- {row['site']} ({row['compartment']}, {row['analyte']}): "
            f"benchmark ratio={row['benchmark_ratio']:.2f}, "
            f"load={load_text}, "
            f"Kd={row['Kd_L_kg']:.3f} L/kg, "
            f"retardation={row['retardation_factor_proxy']:.2f}, "
            f"persistence={row['persistence_factor']:.3f}, "
            f"MC exceedance={row['monte_carlo_exceedance_probability']:.2f}, "
            f"habitability pressure={row['chemical_habitability_pressure_index']:.3f}"
        )

    lines.extend(["", "## Compartment summaries", ""])

    for row in summaries:
        load_text = "NA" if row["total_load_kg_day"] is None else f"{row['total_load_kg_day']:.3f} kg/day"
        lines.append(
            f"- {row['compartment']}: "
            f"mean benchmark ratio={row['mean_benchmark_ratio']:.2f}, "
            f"mean contaminant pressure={row['mean_contaminant_pressure_index']:.3f}, "
            f"mean habitability pressure={row['mean_chemical_habitability_pressure_index']:.3f}, "
            f"mean MC exceedance probability={row['mean_monte_carlo_exceedance_probability']:.2f}, "
            f"total load={load_text}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not regulatory findings, public-health advisories, environmental forensic conclusions, site-remediation designs, legal evidence, ecological risk assessments, drinking-water determinations, hazardous-waste determinations, or operational monitoring products.",
        ]
    )

    (OUT_REPORTS / "advanced_environmental_chemistry_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(
    indicators: list[dict],
    summaries: list[dict],
    decay_series: list[dict],
    leaching_series: list[dict],
    partition_series: list[dict],
    exposure_series: list[dict],
) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "environmental-chemistry-chemical-conditions-habitability",
        "title": "Environmental Chemistry and the Chemical Conditions of Habitability",
        "advanced_layer": True,
        "synthetic_records": len(indicators),
        "summary_groups": len(summaries),
        "decay_scenario_rows": len(decay_series),
        "leaching_scenario_rows": len(leaching_series),
        "partition_scenario_rows": len(partition_series),
        "exposure_scenario_rows": len(exposure_series),
        "outputs": [
            "advanced/outputs/tables/advanced_environmental_chemistry_indicators.csv",
            "advanced/outputs/tables/advanced_compartment_summary.csv",
            "advanced/outputs/tables/advanced_decay_scenario.csv",
            "advanced/outputs/tables/advanced_leaching_retardation_scenarios.csv",
            "advanced/outputs/tables/advanced_multimedia_partition_scenarios.csv",
            "advanced/outputs/tables/advanced_exposure_pathway_scenarios.csv",
            "advanced/outputs/reports/advanced_environmental_chemistry_report.md",
        ],
        "responsible_use": "Synthetic educational environmental chemistry workflow only; not for regulatory, public-health, forensic, legal, remediation, ecological-risk, hazardous-waste, or operational monitoring decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced environmental chemistry workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_compartment(indicators)

    # Use TCE as decay and partition example because it is volatile and persistent enough
    # to show multimedia and decay behavior in the synthetic dataset.
    tce_row = next(row for row in rows if row["analyte"] == "TCE")
    pyrene_row = next(row for row in rows if row["analyte"] == "pyrene")
    arsenic_row = next(row for row in rows if row["analyte"] == "arsenic")

    decay_series = build_decay_scenario(tce_row)
    leaching_series = build_leaching_retardation_scenario(arsenic_row)
    partition_series = build_multimedia_partition_scenario(pyrene_row)
    exposure_series = build_exposure_pathway_scenario(arsenic_row)

    write_csv(OUT_TABLES / "advanced_environmental_chemistry_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_compartment_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_decay_scenario.csv", decay_series)
    write_csv(OUT_TABLES / "advanced_leaching_retardation_scenarios.csv", leaching_series)
    write_csv(OUT_TABLES / "advanced_multimedia_partition_scenarios.csv", partition_series)
    write_csv(OUT_TABLES / "advanced_exposure_pathway_scenarios.csv", exposure_series)

    write_report(indicators, summaries)
    write_manifest(indicators, summaries, decay_series, leaching_series, partition_series, exposure_series)

    print("Advanced environmental chemistry workflow complete.")
    print(f"Records: {len(indicators)}")
    print(f"Compartment summaries: {len(summaries)}")
    print(f"Decay scenario rows: {len(decay_series)}")
    print(f"Leaching scenario rows: {len(leaching_series)}")
    print(f"Partition scenario rows: {len(partition_series)}")
    print(f"Exposure scenario rows: {len(exposure_series)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
