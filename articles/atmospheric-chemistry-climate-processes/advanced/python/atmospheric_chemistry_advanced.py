#!/usr/bin/env python3
"""
Advanced atmospheric chemistry workflow.

Article:
Atmospheric Chemistry and Climate Processes

This script uses synthetic atmospheric chemistry data to calculate:

- benchmark/reference ratios
- greenhouse radiative-forcing proxies
- atmospheric lifetime persistence
- photochemical ozone formation proxies
- aerosol direct-effect proxies
- oxidizing-capacity stress indicators
- composite atmospheric chemistry pressure index
- greenhouse concentration scenario series
- methane lifetime decay series
- ozone photochemical sensitivity scenarios
- aerosol optical-depth sensitivity scenarios
- grouped summaries by chemical class

This is educational scaffolding only. It is not a chemical transport model,
climate attribution model, regulatory air-quality determination, public-health
advisory, emissions inventory, legal analysis, or operational forecast.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "atmospheric_chemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "concentration",
    "reference_concentration",
    "temperature_c",
    "relative_humidity_percent",
    "sunlight_index",
    "nox_ppb",
    "voc_ppb",
    "oh_index",
    "aod",
    "single_scattering_albedo",
    "lifetime_days",
    "background_pressure_hPa",
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
    """Load synthetic atmospheric chemistry records."""
    rows: list[dict] = []

    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append({key: parse_value(key, value) for key, value in row.items()})

    return rows


def reference_ratio(concentration: float, reference_concentration: float) -> float:
    """Calculate concentration / reference concentration."""
    if reference_concentration <= 0:
        return 0.0
    return concentration / reference_concentration


def greenhouse_forcing_proxy(species: str, concentration: float, reference: float) -> float:
    """
    Estimate simplified greenhouse radiative-forcing proxies.

    CO2:
        ΔF = 5.35 ln(C/C0)

    CH4 and N2O:
        simplified square-root forms used for teaching only.

    These are not full IPCC forcing calculations and omit overlap terms.
    """
    if concentration <= 0 or reference <= 0:
        return 0.0

    if species == "CO2":
        return 5.35 * math.log(concentration / reference)

    if species == "CH4":
        return 0.036 * (math.sqrt(concentration) - math.sqrt(reference))

    if species == "N2O":
        return 0.12 * (math.sqrt(concentration) - math.sqrt(reference))

    return 0.0


def lifetime_persistence_factor(lifetime_days: float) -> float:
    """Convert atmospheric lifetime into a bounded persistence proxy."""
    return lifetime_days / (lifetime_days + 30.0)


def photochemical_ozone_index(nox_ppb: float, voc_ppb: float, sunlight_index: float) -> float:
    """
    Estimate a simplified ozone-formation proxy.

    This is a teaching indicator, not a photochemical mechanism.
    """
    if nox_ppb <= 0 or voc_ppb <= 0:
        return 0.0

    return math.sqrt(nox_ppb * voc_ppb) * sunlight_index


def aerosol_direct_effect_proxy(aod: float, single_scattering_albedo: float) -> float:
    """
    Estimate simplified aerosol direct radiative effect proxy.

    Negative values represent scattering/cooling tendency.
    Positive absorbing contribution is included through low single scattering albedo.
    """
    scattering_component = -25.0 * aod * single_scattering_albedo
    absorbing_component = 12.0 * aod * (1.0 - single_scattering_albedo)
    return scattering_component + absorbing_component


def oxidizing_capacity_stress_index(row: dict) -> float:
    """
    Estimate a simplified oxidizing-capacity stress index.

    Higher CO, VOC, and methane burdens combined with lower OH index
    increase the pressure proxy.
    """
    oh = max(row["oh_index"], 0.05)
    reactive_burden = 0.0

    if row["species"] == "CO":
        reactive_burden += reference_ratio(row["concentration"], row["reference_concentration"])

    if row["species"] == "CH4":
        reactive_burden += 0.5 * reference_ratio(row["concentration"], row["reference_concentration"])

    reactive_burden += 0.01 * row["voc_ppb"]

    return clamp(reactive_burden / (4.0 * oh))


def aerosol_pressure_index(row: dict) -> float:
    """Simplified aerosol pressure using concentration and optical depth."""
    concentration_component = clamp(reference_ratio(row["concentration"], row["reference_concentration"]) / 3.0)
    optical_component = clamp(row["aod"] / 0.8)
    absorption_component = clamp((1.0 - row["single_scattering_albedo"]) / 0.25)

    return clamp(
        0.45 * concentration_component
        + 0.35 * optical_component
        + 0.20 * absorption_component
    )


def atmospheric_chemistry_pressure_index(row: dict) -> float:
    """
    Composite atmospheric chemistry pressure index.

    Components:
    - concentration/reference ratio
    - greenhouse forcing proxy
    - atmospheric persistence
    - ozone formation potential
    - aerosol pressure
    - oxidizing-capacity stress
    - QA penalty
    """
    ratio_component = clamp(math.log1p(reference_ratio(row["concentration"], row["reference_concentration"])) / math.log(4.0))

    forcing = greenhouse_forcing_proxy(
        row["species"],
        row["concentration"],
        row["reference_concentration"],
    )
    forcing_component = clamp(abs(forcing) / 4.0)

    persistence_component = lifetime_persistence_factor(row["lifetime_days"])
    ozone_component = clamp(photochemical_ozone_index(row["nox_ppb"], row["voc_ppb"], row["sunlight_index"]) / 100.0)
    aerosol_component = aerosol_pressure_index(row)
    oxidation_component = oxidizing_capacity_stress_index(row)
    qc_penalty = 1.0 - row["qc_score"]

    if row["chemical_class"] == "greenhouse_gas":
        return clamp(
            0.28 * ratio_component
            + 0.32 * forcing_component
            + 0.25 * persistence_component
            + 0.10 * oxidation_component
            + 0.05 * qc_penalty
        )

    if row["chemical_class"] == "aerosol":
        return clamp(
            0.25 * ratio_component
            + 0.20 * persistence_component
            + 0.40 * aerosol_component
            + 0.10 * ozone_component
            + 0.05 * qc_penalty
        )

    if row["chemical_class"] == "secondary_pollutant":
        return clamp(
            0.25 * ratio_component
            + 0.45 * ozone_component
            + 0.10 * aerosol_component
            + 0.10 * oxidation_component
            + 0.10 * qc_penalty
        )

    return clamp(
        0.25 * ratio_component
        + 0.20 * persistence_component
        + 0.20 * ozone_component
        + 0.15 * aerosol_component
        + 0.15 * oxidation_component
        + 0.05 * qc_penalty
    )


def enrich_row(row: dict) -> dict:
    """Add advanced atmospheric chemistry indicators to one row."""
    ratio = reference_ratio(row["concentration"], row["reference_concentration"])
    forcing = greenhouse_forcing_proxy(
        row["species"],
        row["concentration"],
        row["reference_concentration"],
    )
    persistence = lifetime_persistence_factor(row["lifetime_days"])
    ozone_index = photochemical_ozone_index(row["nox_ppb"], row["voc_ppb"], row["sunlight_index"])
    aerosol_effect = aerosol_direct_effect_proxy(row["aod"], row["single_scattering_albedo"])
    aerosol_pressure = aerosol_pressure_index(row)
    oxidation_stress = oxidizing_capacity_stress_index(row)
    pressure = atmospheric_chemistry_pressure_index(row)

    if pressure >= 0.65:
        attention_flag = "high_attention"
    elif pressure >= 0.45:
        attention_flag = "moderate_attention"
    else:
        attention_flag = "monitor"

    return {
        **row,
        "reference_ratio": ratio,
        "greenhouse_forcing_proxy_W_m2": forcing,
        "lifetime_persistence_factor": persistence,
        "photochemical_ozone_index": ozone_index,
        "aerosol_direct_effect_proxy": aerosol_effect,
        "aerosol_pressure_index": aerosol_pressure,
        "oxidizing_capacity_stress_index": oxidation_stress,
        "atmospheric_chemistry_pressure_index": pressure,
        "evidence_weighted_pressure_index": pressure * row["qc_score"],
        "attention_flag": attention_flag,
    }


def summarize_by_chemical_class(indicators: list[dict]) -> list[dict]:
    """Summarize indicators by chemical class."""
    grouped: dict[str, list[dict]] = {}

    for row in indicators:
        grouped.setdefault(row["chemical_class"], []).append(row)

    summaries: list[dict] = []

    for chemical_class, records in sorted(grouped.items()):
        summaries.append(
            {
                "chemical_class": chemical_class,
                "n": len(records),
                "mean_reference_ratio": mean(row["reference_ratio"] for row in records),
                "mean_greenhouse_forcing_proxy_W_m2": mean(row["greenhouse_forcing_proxy_W_m2"] for row in records),
                "mean_lifetime_persistence_factor": mean(row["lifetime_persistence_factor"] for row in records),
                "mean_photochemical_ozone_index": mean(row["photochemical_ozone_index"] for row in records),
                "mean_aerosol_pressure_index": mean(row["aerosol_pressure_index"] for row in records),
                "mean_atmospheric_chemistry_pressure_index": mean(row["atmospheric_chemistry_pressure_index"] for row in records),
            }
        )

    return summaries


def build_greenhouse_scenario_series() -> list[dict]:
    """
    Build greenhouse forcing scenario series for CO2, CH4, and N2O.

    This is a teaching series, not a climate projection.
    """
    rows: list[dict] = []

    scenarios = [
        ("CO2", 280.0, [280, 350, 420, 500, 650, 800], "ppm"),
        ("CH4", 722.0, [722, 1000, 1500, 1950, 2400, 3000], "ppb"),
        ("N2O", 270.0, [270, 300, 337, 380, 430, 500], "ppb"),
    ]

    for species, reference, concentrations, unit in scenarios:
        for concentration in concentrations:
            rows.append(
                {
                    "scenario": "greenhouse_forcing",
                    "species": species,
                    "concentration": concentration,
                    "reference_concentration": reference,
                    "unit": unit,
                    "forcing_proxy_W_m2": greenhouse_forcing_proxy(species, concentration, reference),
                }
            )

    return rows


def build_methane_lifetime_decay_series(initial_ppb: float = 1950.0, lifetime_days: float = 4380.0) -> list[dict]:
    """Build a first-order methane perturbation decay series."""
    rows: list[dict] = []

    for year in range(0, 61, 2):
        days = year * 365.25
        concentration = initial_ppb * math.exp(-days / lifetime_days)

        rows.append(
            {
                "scenario": "methane_lifetime_decay",
                "year": year,
                "modeled_CH4_ppb": concentration,
                "fraction_remaining": concentration / initial_ppb,
                "lifetime_days": lifetime_days,
            }
        )

    return rows


def build_ozone_photochemical_scenario_series() -> list[dict]:
    """Build ozone-production proxy scenarios across NOx, VOC, and sunlight."""
    rows: list[dict] = []

    nox_values = [5, 15, 30, 60]
    voc_values = [20, 50, 100, 180]
    sunlight_values = [0.5, 1.0, 1.3]

    for nox in nox_values:
        for voc in voc_values:
            for sunlight in sunlight_values:
                rows.append(
                    {
                        "scenario": "ozone_photochemical_sensitivity",
                        "nox_ppb": nox,
                        "voc_ppb": voc,
                        "sunlight_index": sunlight,
                        "photochemical_ozone_index": photochemical_ozone_index(nox, voc, sunlight),
                    }
                )

    return rows


def build_aerosol_optical_scenario_series() -> list[dict]:
    """Build aerosol direct-effect proxy scenarios."""
    rows: list[dict] = []

    aod_values = [0.03, 0.10, 0.25, 0.50, 0.80]
    ssa_values = [0.82, 0.90, 0.96, 0.99]

    for aod in aod_values:
        for ssa in ssa_values:
            rows.append(
                {
                    "scenario": "aerosol_optical_sensitivity",
                    "aod": aod,
                    "single_scattering_albedo": ssa,
                    "aerosol_direct_effect_proxy": aerosol_direct_effect_proxy(aod, ssa),
                    "aerosol_pressure_index": clamp(0.55 * clamp(aod / 0.8) + 0.45 * clamp((1.0 - ssa) / 0.25)),
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

    greenhouse_records = [
        row for row in indicators
        if row["chemical_class"] == "greenhouse_gas"
    ]

    aerosol_records = [
        row for row in indicators
        if row["chemical_class"] == "aerosol"
    ]

    lines = [
        "# Advanced Atmospheric Chemistry Report",
        "",
        "This report summarizes synthetic atmospheric chemistry indicators for the article **Atmospheric Chemistry and Climate Processes**.",
        "",
        f"Total records: {len(indicators)}",
        f"Greenhouse gas records: {len(greenhouse_records)}",
        f"Aerosol records: {len(aerosol_records)}",
        f"High attention records: {len(high_attention)}",
        f"Moderate attention records: {len(moderate_attention)}",
        "",
        "## High attention records",
        "",
    ]

    for row in high_attention:
        lines.append(
            f"- {row['station']} ({row['species']}, {row['chemical_class']}): "
            f"ratio={row['reference_ratio']:.2f}, "
            f"forcing proxy={row['greenhouse_forcing_proxy_W_m2']:.3f} W/m2, "
            f"ozone index={row['photochemical_ozone_index']:.2f}, "
            f"aerosol pressure={row['aerosol_pressure_index']:.3f}, "
            f"pressure index={row['atmospheric_chemistry_pressure_index']:.3f}"
        )

    lines.extend(["", "## Chemical-class summaries", ""])

    for row in summaries:
        lines.append(
            f"- {row['chemical_class']}: "
            f"mean ratio={row['mean_reference_ratio']:.2f}, "
            f"mean forcing proxy={row['mean_greenhouse_forcing_proxy_W_m2']:.3f} W/m2, "
            f"mean ozone index={row['mean_photochemical_ozone_index']:.2f}, "
            f"mean pressure index={row['mean_atmospheric_chemistry_pressure_index']:.3f}"
        )

    lines.extend(
        [
            "",
            "## Responsible-use note",
            "",
            "These results are synthetic and educational. They are not chemical transport model outputs, climate-attribution findings, regulatory air-quality determinations, public-health advisories, emissions inventories, legal evidence, or operational forecasts.",
        ]
    )

    (OUT_REPORTS / "advanced_atmospheric_chemistry_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest(
    indicators: list[dict],
    summaries: list[dict],
    greenhouse_series: list[dict],
    methane_series: list[dict],
    ozone_series: list[dict],
    aerosol_series: list[dict],
) -> None:
    """Write output provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "atmospheric-chemistry-climate-processes",
        "title": "Atmospheric Chemistry and Climate Processes",
        "advanced_layer": True,
        "synthetic_records": len(indicators),
        "summary_groups": len(summaries),
        "greenhouse_scenario_rows": len(greenhouse_series),
        "methane_decay_rows": len(methane_series),
        "ozone_scenario_rows": len(ozone_series),
        "aerosol_scenario_rows": len(aerosol_series),
        "outputs": [
            "advanced/outputs/tables/advanced_atmospheric_chemistry_indicators.csv",
            "advanced/outputs/tables/advanced_chemical_class_summary.csv",
            "advanced/outputs/tables/advanced_greenhouse_forcing_scenarios.csv",
            "advanced/outputs/tables/advanced_methane_lifetime_decay.csv",
            "advanced/outputs/tables/advanced_ozone_photochemical_scenarios.csv",
            "advanced/outputs/tables/advanced_aerosol_optical_scenarios.csv",
            "advanced/outputs/reports/advanced_atmospheric_chemistry_report.md",
        ],
        "responsible_use": "Synthetic educational atmospheric chemistry workflow only; not for regulatory, public-health, legal, climate-attribution, emissions inventory, or operational forecasting decisions.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    """Run the full advanced atmospheric chemistry workflow."""
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    summaries = summarize_by_chemical_class(indicators)

    greenhouse_series = build_greenhouse_scenario_series()
    methane_series = build_methane_lifetime_decay_series()
    ozone_series = build_ozone_photochemical_scenario_series()
    aerosol_series = build_aerosol_optical_scenario_series()

    write_csv(OUT_TABLES / "advanced_atmospheric_chemistry_indicators.csv", indicators)
    write_csv(OUT_TABLES / "advanced_chemical_class_summary.csv", summaries)
    write_csv(OUT_TABLES / "advanced_greenhouse_forcing_scenarios.csv", greenhouse_series)
    write_csv(OUT_TABLES / "advanced_methane_lifetime_decay.csv", methane_series)
    write_csv(OUT_TABLES / "advanced_ozone_photochemical_scenarios.csv", ozone_series)
    write_csv(OUT_TABLES / "advanced_aerosol_optical_scenarios.csv", aerosol_series)

    write_report(indicators, summaries)
    write_manifest(indicators, summaries, greenhouse_series, methane_series, ozone_series, aerosol_series)

    print("Advanced atmospheric chemistry workflow complete.")
    print(f"Records: {len(indicators)}")
    print(f"Chemical-class summaries: {len(summaries)}")
    print(f"Greenhouse scenario rows: {len(greenhouse_series)}")
    print(f"Methane decay rows: {len(methane_series)}")
    print(f"Ozone scenario rows: {len(ozone_series)}")
    print(f"Aerosol scenario rows: {len(aerosol_series)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
