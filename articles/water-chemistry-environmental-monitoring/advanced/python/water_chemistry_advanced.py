#!/usr/bin/env python3
"""
Advanced water chemistry workflow.

Article:
Water Chemistry and Environmental Monitoring

This script uses synthetic water monitoring data to calculate:

- benchmark ratios
- concentration-to-load conversion
- dissolved oxygen deficit
- pH pressure
- conductivity pressure
- turbidity pressure
- nutrient enrichment index
- metal pressure index
- QA-weighted water-quality pressure
- storm-pulse first-order decay series
- nutrient-load scenario series
- dissolved-oxygen sag scenario series
- grouped summaries by water body type

This is educational scaffolding only. It is not a regulatory compliance tool,
drinking-water safety determination, watershed permit model, public-health
advisory, legal analysis, or operational monitoring system.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "water_chemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "concentration",
    "benchmark",
    "flow_L_s",
    "temperature_c",
    "pH",
    "specific_conductance_uS_cm",
    "dissolved_oxygen_mg_L",
    "do_saturation_mg_L",
    "turbidity_NTU",
    "nitrate_mg_L",
    "phosphate_mg_L",
    "chloride_mg_L",
    "lead_ug_L",
    "copper_ug_L",
    "arsenic_ug_L",
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
    """Load synthetic water chemistry monitoring records."""
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


def oxygen_deficit_mg_L(dissolved_oxygen_mg_L: float, do_saturation_mg_L: float) -> float:
    """Calculate dissolved oxygen deficit relative to saturation."""
    return max(do_saturation_mg_L - dissolved_oxygen_mg_L, 0.0)


def oxygen_stress_index(dissolved_oxygen_mg_L: float, do_saturation_mg_L: float) -> float:
    """
    Estimate oxygen stress.

    Low dissolved oxygen and large oxygen deficit increase the index.
    """
    low_do_component = clamp((6.0 - dissolved_oxygen_mg_L) / 6.0)
    deficit_component = clamp(oxygen_deficit_mg_L(dissolved_oxygen_mg_L, do_saturation_mg_L) / 6.0)

    return clamp(0.60 * low_do_component + 0.40 * deficit_component)


def pH_pressure(pH: float) -> float:
    """Simplified pressure from low or high pH."""
    if pH < 6.5:
        return clamp((6.5 - pH) / 2.0)
    if pH > 8.5:
        return clamp((pH - 8.5) / 2.0)
    return 0.0


def conductivity_pressure(specific_conductance_uS_cm: float) -> float:
    """Simplified ionic-strength/salinity pressure proxy."""
    return clamp((specific_conductance_uS_cm - 750.0) / 3000.0)


def turbidity_pressure(turbidity_NTU: float) -> float:
    """Simplified turbidity and suspended-material pressure."""
    return clamp(turbidity_NTU / 100.0)


def nutrient_enrichment_index(nitrate_mg_L: float, phosphate_mg_L: float) -> float:
    """Simplified nutrient enrichment index."""
    nitrate_component = clamp(nitrate_mg_L / 10.0)
    phosphate_component = clamp(phosphate_mg_L / 0.20)

    return clamp(0.50 * nitrate_component + 0.50 * phosphate_component)


def metal_pressure_index(lead_ug_L: float, copper_ug_L: float, arsenic_ug_L: float) -> float:
    """Simplified metal/metalloid pressure index."""
    lead_component = clamp(lead_ug_L / 15.0)
    copper_component = clamp(copper_ug_L / 13.0)
    arsenic_component = clamp(arsenic_ug_L / 10.0)

    return clamp(0.34 * lead_component + 0.33 * copper_component + 0.33 * arsenic_component)


def chloride_pressure(chloride_mg_L: float) -> float:
    """Simplified chloride pressure proxy."""
    return clamp((chloride_mg_L - 100.0) / 500.0)


def water_quality_pressure_index(row: dict) -> float:
    """
    Composite water-quality pressure index.

    Components:
    - benchmark exceedance
    - oxygen stress
    - nutrient enrichment
    - metal pressure
    - turbidity
    - conductivity/chloride
    - pH pressure
    - QA penalty
    """
    ratio_component = clamp(math.log1p(benchmark_ratio(row["concentration"], row["benchmark"])) / math.log(4.0))
    oxygen_component = oxygen_stress_index(row["dissolved_oxygen_mg_L"], row["do_saturation_mg_L"])
    nutrient_component = nutrient_enrichment_index(row["nitrate_mg_L"], row["phosphate_mg_L"])
    metal_component = metal_pressure_index(row["lead_ug_L"], row["copper_ug_L"], row["arsenic_ug_L"])
    turbidity_component = turbidity_pressure(row["turbidity_NTU"])
    ionic_component = max(
        conductivity_pressure(row["specific_conductance_uS_cm"]),
        chloride_pressure(row["chloride_mg_L"]),
    )
    ph_component = pH_pressure(row["pH"])
    qc_penalty = 1.0 - row["qc_score"]

    return clamp(
        0.20 * ratio_component
        + 0.18 * oxygen_component
        + 0.18 * nutrient_component
        + 0.16 * metal_component
        + 0.10 * turbidity_component
        + 0.08 * ionic_component
        + 0.05 * ph_component
        + 0.05 * qc_penalty
    )


def enrich_row(row: dict) -> dict:
    """Add advanced water chemistry indicators to one row."""
    ratio = benchmark_ratio(row["concentration"], row["benchmark"])
    load = concentration_load_kg_day(row["concentration"], row["unit"], row["flow_L_s"])
    oxygen_deficit = oxygen_deficit_mg_L(row["dissolved_oxygen_mg_L"], row["do_saturation_mg_L"])
    oxygen_stress = oxygen_stress_index(row["dissolved_oxygen_mg_L"], row["do_saturation_mg_L"])
    nutrient_index = nutrient_enrichment_index(row["nitrate_mg_L"], row["phosphate_mg_L"])
    metal_index = metal_pressure_index(row["lead_ug_L"], row["copper_ug_L"], row["arsenic_ug_L"])
    pressure = water_quality_pressure_index(row)

    if pressure >= 0.65:
        attention_flag = "high_attention"
    elif pressure >= 0.45:
        attention_flag = "moderate_attention"
    else:
        attention_flag = "monitor"

    return {
        **row,
        "benchmark_ratio": ratio,
        "load_kg_day": load,
        "oxygen_deficit_mg_L": oxygen_deficit,
        "oxygen_stress_index": oxygen_stress,
        "pH_pressure": pH_pressure(row["pH"]),
        "conductivity_pressure": conductivity_pressure(row["specific_conductance_uS_cm"]),
        "chloride_pressure": chloride_pressure(row["chloride_mg_L"]),
        "turbidity_pressure": turbidity_pressure(row["turbidity_NTU"]),
        "nutrient_enrichment_index": nutrient_index,
        "metal_pressure_index": metal_index,
        "water_quality_pressure_index": pressure,
        "evidence_weighted_pressure_index": pressure * row["qc_score"],
        "attention_flag": attention_flag,
    }


def summarize_by_water_body_type(indicators: list[dict]) -> list[dict]:
    """Summarize indicators by water body type."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["water_body_type"], []).append(row)

    summaries: list[dict] = []

    for water_body_type, records in sorted(grouped.items()):
        loads = [row["load_kg_day"] for row in records if row["load_kg_day"] is not None]

        summaries.append(
            {
                "water_body_type": water_body_type,
                "n": len(records),
                "mean_pH": mean(row["pH"] for row in records),
                "mean_dissolved_oxygen_mg_L": mean(row["dissolved_oxygen_mg_L"] for row in records),
                "mean_oxygen_stress_index": mean(row["oxygen_stress_index"] for row in records),
                "mean_nutrient_enrichment_index": mean(row["nutrient_enrichment_index"] for row in records),
                "mean_metal_pressure_index": mean(row["metal_pressure_index"] for row in records),
                "mean_turbidity_pressure": mean(row["turbidity_pressure"] for row in records),
                "mean_water_quality_pressure_index": mean(row["water_quality_pressure_index"] for row in records),
                "total_load_kg_day": sum(loads) if loads else None,
            }
        )

    return summaries


def build_storm_pulse_decay_series(base_row: dict) -> list[dict]:
    """
    Build a first-order storm-pulse concentration decay series.

    This represents dilution/settling/decay as a teaching model.
    """
    rows: list[dict] = []

    initial_concentration = base_row["concentration"]
    half_life_hours = 12.0
    decay_constant = math.log(2.0) / half_life_hours

    for hour in range(0, 73, 3):
        concentration = initial_concentration * math.exp(-decay_constant * hour)

        rows.append(
            {
                "scenario": "storm_pulse_decay",
                "site": base_row["site"],
                "hour": hour,
                "modeled_concentration": concentration,
                "unit": base_row["unit"],
                "fraction_remaining": concentration / initial_concentration if initial_concentration else 0.0,
            }
        )

    return rows


def build_nutrient_load_scenarios(base_row: dict) -> list[dict]:
    """Build nutrient load scenarios across flow and concentration multipliers."""
    rows: list[dict] = []

    concentration_multipliers = [0.50, 0.75, 1.00, 1.25, 1.50]
    flow_multipliers = [0.50, 1.00, 2.00, 3.00]

    for concentration_multiplier in concentration_multipliers:
        for flow_multiplier in flow_multipliers:
            concentration = base_row["concentration"] * concentration_multiplier
            flow = base_row["flow_L_s"] * flow_multiplier
            load = concentration_load_kg_day(concentration, base_row["unit"], flow)

            rows.append(
                {
                    "scenario": "nutrient_load",
                    "site": base_row["site"],
                    "concentration_multiplier": concentration_multiplier,
                    "flow_multiplier": flow_multiplier,
                    "modeled_concentration": concentration,
                    "modeled_flow_L_s": flow,
                    "modeled_load_kg_day": load,
                    "unit": base_row["unit"],
                }
            )

    return rows


def build_dissolved_oxygen_sag_series(base_row: dict) -> list[dict]:
    """
    Build a simple dissolved-oxygen sag and recovery scenario.

    This is a teaching model, not a Streeter-Phelps implementation.
    """
    rows: list[dict] = []

    initial_do = base_row["do_saturation_mg_L"]
    max_deficit = max(base_row["do_saturation_mg_L"] - base_row["dissolved_oxygen_mg_L"], 1.5)
    recovery_rate = 0.045

    for hour in range(0, 121, 6):
        # Deficit peaks early, then decays.
        deficit = max_deficit * math.exp(-recovery_rate * hour)
        modeled_do = max(initial_do - deficit, 0.0)

        rows.append(
            {
                "scenario": "dissolved_oxygen_sag",
                "site": base_row["site"],
                "hour": hour,
                "modeled_dissolved_oxygen_mg_L": modeled_do,
                "modeled_oxygen_deficit_mg_L": deficit,
                "oxygen_stress_index": oxygen_stress_index(modeled_do, base_row["do_saturation_mg_L"]),
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

    low_oxygen = [
        row for row in indicators
        if row["dissolved_oxygen_mg_L"] < 5.0
    ]

    lines = [
        "# Advanced Water Chemistry Report",
        "",
        "This report summarizes synthetic water chemistry indicators for the article **Water Chemistry and Environmental Monitoring**.",
        "",
        f"Total records: {len(indicators)}",
        f"Benchmark exceedances: {len(benchmark_exceedances)}",
        f"Low dissolved oxygen records: {len(low_oxygen)}",
        f"High attention records: {len(high_attention)}",
        f"Moderate attention records: {len(moderate_attention)}",
        "",
        "## High attention records",
        "",
    ]

    for row in high_attention:
        load_text = "NA" if row["load_kg_day"] is None else f"{row['load_kg_day']:.2f} kg/day"
        lines.append(
            f"- {row['site']} ({row['water_body_type']}): "
            f"analyte={row['analyte']}, "
            f"benchmark ratio={row['benchmark_ratio']:.2f}, "
            f"load={load_text}, "
            f"oxygen stress={row['oxygen_stress_index']:.3f}, "
            f"nutrient index={row['nutrient_enrichment_index']:.3f}, "
            f"metal index={row['metal_pressure_index']:.3f}, "
            f"pressure index={row['water_quality_pressure_index']:.3f}"
        )

    lines.extend(["", "## Water-body summaries", ""])

    for row in summaries:
        load_text = "NA" if row["total_load_kg_day"] is None else f"{row['total_load_kg_day']:.2f} kg/day"
        lines.append(
            f"- {row['water_body_type']}: "
            f"mean DO={row['mean_dissolved_oxygen_mg_L']:.2f} mg/L, "
            f"mean nutrient index={row['mean_nutrient_enrichment_index']:.3f}, "
            f"mean metal index={row['mean_metal_pressure_index']:.3f}, "
            f"mean pressure index={row['mean_water_quality_pressure_index']:.3f}, "
            f"total load={load_text}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not regulatory findings, drinking-water safety determinations, public-health advisories, legal evidence, watershed permit models, or operational monitoring products.",
        ]
    )

    (OUT_REPORTS / "advanced_water_chemistry_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(
    indicators: list[dict],
    summaries: list[dict],
    storm_series: list[dict],
    nutrient_series: list[dict],
    oxygen_series: list[dict],
) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "water-chemistry-environmental-monitoring",
        "title": "Water Chemistry and Environmental Monitoring",
        "advanced_layer": True,
        "synthetic_records": len(indicators),
        "summary_groups": len(summaries),
        "storm_pulse_rows": len(storm_series),
        "nutrient_load_scenario_rows": len(nutrient_series),
        "oxygen_sag_rows": len(oxygen_series),
        "outputs": [
            "advanced/outputs/tables/advanced_water_chemistry_indicators.csv",
            "advanced/outputs/tables/advanced_water_body_summary.csv",
            "advanced/outputs/tables/advanced_storm_pulse_decay.csv",
            "advanced/outputs/tables/advanced_nutrient_load_scenarios.csv",
            "advanced/outputs/tables/advanced_dissolved_oxygen_sag.csv",
            "advanced/outputs/reports/advanced_water_chemistry_report.md",
        ],
        "responsible_use": "Synthetic educational water chemistry workflow only; not for regulatory, drinking-water, public-health, legal, permit, or operational monitoring decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced water chemistry workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_water_body_type(indicators)

    storm_row = next(row for row in rows if row["site"] == "Storm-D")
    nutrient_row = next(row for row in rows if row["analyte"] == "nitrate_as_N")
    oxygen_row = next(row for row in rows if row["site"] == "Lake-B")

    storm_series = build_storm_pulse_decay_series(storm_row)
    nutrient_series = build_nutrient_load_scenarios(nutrient_row)
    oxygen_series = build_dissolved_oxygen_sag_series(oxygen_row)

    write_csv(OUT_TABLES / "advanced_water_chemistry_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_water_body_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_storm_pulse_decay.csv", storm_series)
    write_csv(OUT_TABLES / "advanced_nutrient_load_scenarios.csv", nutrient_series)
    write_csv(OUT_TABLES / "advanced_dissolved_oxygen_sag.csv", oxygen_series)

    write_report(indicators, summaries)
    write_manifest(indicators, summaries, storm_series, nutrient_series, oxygen_series)

    print("Advanced water chemistry workflow complete.")
    print(f"Records: {len(indicators)}")
    print(f"Water-body summaries: {len(summaries)}")
    print(f"Storm pulse rows: {len(storm_series)}")
    print(f"Nutrient scenario rows: {len(nutrient_series)}")
    print(f"Oxygen sag rows: {len(oxygen_series)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
