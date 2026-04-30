#!/usr/bin/env python3
"""
Ocean carbonate chemistry workflow:
- Load synthetic ocean carbonate monitoring data.
- Estimate simplified carbonate species fractions.
- Estimate carbonate ion concentration.
- Screen simplified aragonite saturation state.
- Estimate an illustrative air-sea CO2 flux proxy.
- Write output tables, report, and provenance manifest.

Educational only. Not for research-grade carbonate chemistry, operational
monitoring, regulatory decisions, hatchery management, climate attribution,
or legal evidence.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "ocean_carbonate_monitoring_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"


NUMERIC_FIELDS = [
    "latitude",
    "longitude",
    "depth_m",
    "temperature_c",
    "salinity",
    "pH_total_scale",
    "DIC_umol_kg",
    "total_alkalinity_umol_kg",
    "pCO2_uatm",
    "calcium_mmol_kg",
    "oxygen_umol_kg",
    "nitrate_umol_kg",
    "phosphate_umol_kg",
    "silicate_umol_kg",
]


# Simplified teaching constants.
# Research-grade workflows must use temperature-, salinity-, pressure-,
# nutrient-, and pH-scale-dependent constants.
K1 = 10.0 ** -6.0
K2 = 10.0 ** -9.1
KSP_ARAGONITE = 6.5e-7
KSP_CALCITE = 4.4e-7


def parse_float(value: str) -> float | None:
    value = value.strip()
    if value == "" or value.upper() == "NA":
        return None
    return float(value)


def load_rows() -> list[dict]:
    rows = []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for field in NUMERIC_FIELDS:
                row[field] = parse_float(row[field])
            rows.append(row)
    return rows


def carbonate_fractions(pH: float) -> tuple[float, float, float]:
    """
    Simplified carbonate alpha fractions.

    alpha0 = CO2* fraction
    alpha1 = HCO3- fraction
    alpha2 = CO3-- fraction
    """
    h = 10.0 ** (-pH)
    denominator = h**2 + K1 * h + K1 * K2
    alpha0 = h**2 / denominator
    alpha1 = K1 * h / denominator
    alpha2 = K1 * K2 / denominator
    return alpha0, alpha1, alpha2


def saturation_state(calcium_mmol_kg: float, carbonate_umol_kg: float, ksp: float) -> float:
    """Calculate simplified calcium carbonate saturation state."""
    calcium_mol_kg = calcium_mmol_kg * 1.0e-3
    carbonate_mol_kg = carbonate_umol_kg * 1.0e-6
    return calcium_mol_kg * carbonate_mol_kg / ksp


def co2_flux_proxy(pco2_water_uatm: float, pco2_air_uatm: float = 420.0, gas_transfer_factor: float = 1.0) -> float:
    """
    Simple air-sea CO2 flux proxy.

    Positive values here mean ocean-to-atmosphere outgassing potential.
    """
    return gas_transfer_factor * (pco2_water_uatm - pco2_air_uatm)


def add_carbonate_indicators(rows: list[dict]) -> list[dict]:
    enriched = []

    for row in rows:
        item = dict(row)
        alpha0, alpha1, alpha2 = carbonate_fractions(row["pH_total_scale"])

        item["alpha_CO2_star"] = alpha0
        item["alpha_HCO3"] = alpha1
        item["alpha_CO3"] = alpha2

        item["CO2_star_umol_kg"] = alpha0 * row["DIC_umol_kg"]
        item["bicarbonate_umol_kg"] = alpha1 * row["DIC_umol_kg"]
        item["carbonate_umol_kg"] = alpha2 * row["DIC_umol_kg"]

        item["omega_aragonite_simplified"] = saturation_state(
            row["calcium_mmol_kg"],
            item["carbonate_umol_kg"],
            KSP_ARAGONITE,
        )
        item["omega_calcite_simplified"] = saturation_state(
            row["calcium_mmol_kg"],
            item["carbonate_umol_kg"],
            KSP_CALCITE,
        )

        item["saturation_flag"] = (
            "low_aragonite_saturation_attention"
            if item["omega_aragonite_simplified"] < 2.0
            else "higher_aragonite_saturation_screen"
        )
        item["co2_flux_proxy_uatm"] = co2_flux_proxy(row["pCO2_uatm"])
        item["flux_direction_screen"] = (
            "outgassing_potential"
            if item["co2_flux_proxy_uatm"] > 0
            else "uptake_potential"
        )

        enriched.append(item)

    return enriched


def summarize_by_water_type(rows: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row["water_type"], []).append(row)

    summary = []
    for water_type, records in sorted(groups.items()):
        summary.append(
            {
                "water_type": water_type,
                "n": len(records),
                "mean_pH_total_scale": mean(row["pH_total_scale"] for row in records),
                "mean_DIC_umol_kg": mean(row["DIC_umol_kg"] for row in records),
                "mean_total_alkalinity_umol_kg": mean(row["total_alkalinity_umol_kg"] for row in records),
                "mean_carbonate_umol_kg": mean(row["carbonate_umol_kg"] for row in records),
                "mean_omega_aragonite_simplified": mean(row["omega_aragonite_simplified"] for row in records),
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict], summary: list[dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    low_sat = [row for row in rows if row["saturation_flag"] == "low_aragonite_saturation_attention"]
    outgassing = [row for row in rows if row["flux_direction_screen"] == "outgassing_potential"]

    lines = [
        "# Ocean Carbonate Chemistry Screening Report",
        "",
        "This educational report summarizes synthetic ocean carbonate monitoring records.",
        "",
        f"Total records: {len(rows)}",
        f"Low aragonite saturation attention flags: {len(low_sat)}",
        f"Outgassing-potential screens: {len(outgassing)}",
        "",
        "## Low aragonite saturation attention flags",
        "",
    ]

    for row in low_sat:
        lines.append(
            f"- {row['station']} | {row['water_type']} | pH={row['pH_total_scale']} | "
            f"Omega_arag={row['omega_aragonite_simplified']:.2f} | carbonate={row['carbonate_umol_kg']:.1f} umol/kg"
        )

    lines.extend(
        [
            "",
            "## Water-type summary",
            "",
        ]
    )

    for row in summary:
        lines.append(
            f"- {row['water_type']} | mean pH={row['mean_pH_total_scale']:.2f} | "
            f"mean Omega_arag={row['mean_omega_aragonite_simplified']:.2f}"
        )

    lines.extend(
        [
            "",
            "This report is educational and is not a research-grade carbonate-system calculation, operational monitoring product, regulatory determination, hatchery advisory, or legal analysis.",
        ]
    )

    (REPORT_DIR / "ocean_carbonate_screening_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "ocean-chemistry-carbonate-system",
        "workflow": "ocean_carbonate_screening.py",
        "data_source": "synthetic educational ocean carbonate monitoring data",
        "generated_outputs": [
            "outputs/tables/ocean_carbonate_indicators.csv",
            "outputs/tables/ocean_water_type_summary.csv",
            "outputs/reports/ocean_carbonate_screening_report.md",
        ],
        "responsible_use": "Educational only; not for research-grade carbonate chemistry, operational monitoring, hatchery decisions, climate attribution, legal, or regulatory decisions.",
    }

    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = add_carbonate_indicators(rows)
    summary = summarize_by_water_type(indicators)

    write_csv(TABLE_DIR / "ocean_carbonate_indicators.csv", indicators)
    write_csv(TABLE_DIR / "ocean_water_type_summary.csv", summary)
    write_report(indicators, summary)
    write_manifest()

    print("Ocean carbonate chemistry workflow complete.")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
