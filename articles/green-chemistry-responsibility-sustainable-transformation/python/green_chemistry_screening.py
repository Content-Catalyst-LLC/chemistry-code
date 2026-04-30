#!/usr/bin/env python3
"""
Green Chemistry, Responsibility, and Sustainable Transformation

Synthetic educational workflow for green chemistry metrics:
- atom economy
- E-factor
- process mass intensity
- solvent burden
- hazard-weighted mass intensity
- energy intensity
- catalysis score
- renewable feedstock score
- circularity and degradation score
- accident prevention and monitoring score
- composite green chemistry score

Not a certification, regulatory, industrial, safety, LCA, or product-claim tool.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "green_chemistry_full_stack_synthetic.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_REPORTS = ROOT / "outputs" / "reports"
OUT_MANIFESTS = ROOT / "outputs" / "manifests"

NUMERIC = {
    "product_mass_kg",
    "product_mw",
    "reactant_mw_sum",
    "total_input_mass_kg",
    "waste_mass_kg",
    "solvent_mass_kg",
    "water_mass_kg",
    "energy_kwh",
    "reaction_temperature_c",
    "reaction_pressure_bar",
    "catalyst_loading_mol_percent",
    "yield_fraction",
    "hazard_score",
    "solvent_hazard_score",
    "renewable_feedstock_fraction",
    "circularity_score",
    "degradation_score",
    "accident_potential_score",
    "realtime_monitoring_score",
    "qc_score",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def parse_row(row: dict) -> dict:
    return {k: float(v) if k in NUMERIC else v for k, v in row.items()}


def load_rows() -> list[dict]:
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        return [parse_row(row) for row in csv.DictReader(handle)]


def atom_economy(row: dict) -> float:
    if row["reactant_mw_sum"] <= 0:
        return 0.0
    return row["product_mw"] / row["reactant_mw_sum"]


def e_factor(row: dict) -> float:
    if row["product_mass_kg"] <= 0:
        return 0.0
    return row["waste_mass_kg"] / row["product_mass_kg"]


def process_mass_intensity(row: dict) -> float:
    if row["product_mass_kg"] <= 0:
        return 0.0
    return row["total_input_mass_kg"] / row["product_mass_kg"]


def solvent_burden(row: dict) -> float:
    if row["product_mass_kg"] <= 0:
        return 0.0
    return row["solvent_mass_kg"] / row["product_mass_kg"]


def hazard_weighted_mass_intensity(row: dict) -> float:
    return process_mass_intensity(row) * (0.60 * row["hazard_score"] + 0.40 * row["solvent_hazard_score"])


def energy_intensity(row: dict) -> float:
    if row["product_mass_kg"] <= 0:
        return 0.0
    return row["energy_kwh"] / row["product_mass_kg"]


def catalysis_score(row: dict) -> float:
    if row["catalyst_loading_mol_percent"] <= 0:
        return 0.0
    return clamp(1.0 - row["catalyst_loading_mol_percent"] / 20.0)


def process_safety_score(row: dict) -> float:
    temperature_pressure = clamp((row["reaction_temperature_c"] - 25.0) / 175.0) * 0.5 + clamp((row["reaction_pressure_bar"] - 1.0) / 20.0) * 0.5
    accident_prevention = 1.0 - row["accident_potential_score"]
    monitoring = row["realtime_monitoring_score"]
    return clamp(0.45 * accident_prevention + 0.35 * monitoring + 0.20 * (1.0 - temperature_pressure))


def green_chemistry_score(row: dict) -> float:
    ae = clamp(atom_economy(row))
    waste = clamp(1.0 - e_factor(row) / 25.0)
    pmi = clamp(1.0 - process_mass_intensity(row) / 30.0)
    hazard = clamp(1.0 - row["hazard_score"])
    solvent = clamp(1.0 - row["solvent_hazard_score"])
    energy = clamp(1.0 - energy_intensity(row) / 60.0)
    catalysis = catalysis_score(row)
    renewable = row["renewable_feedstock_fraction"]
    circular = 0.5 * row["circularity_score"] + 0.5 * row["degradation_score"]
    safety = process_safety_score(row)

    return clamp(
        0.14 * ae +
        0.14 * waste +
        0.12 * pmi +
        0.13 * hazard +
        0.10 * solvent +
        0.09 * energy +
        0.08 * catalysis +
        0.08 * renewable +
        0.08 * circular +
        0.04 * safety
    )


def flag(row: dict) -> str:
    score = row["green_chemistry_score"]
    if score >= 0.70:
        return "strong_green_design_profile"
    if score >= 0.50:
        return "moderate_profile_with_tradeoffs"
    return "redesign_priority"


def enrich(row: dict) -> dict:
    enriched = {
        **row,
        "atom_economy": atom_economy(row),
        "e_factor": e_factor(row),
        "process_mass_intensity": process_mass_intensity(row),
        "solvent_burden": solvent_burden(row),
        "hazard_weighted_mass_intensity": hazard_weighted_mass_intensity(row),
        "energy_intensity_kwh_per_kg_product": energy_intensity(row),
        "catalysis_score": catalysis_score(row),
        "process_safety_score": process_safety_score(row),
        "green_chemistry_score": green_chemistry_score(row),
    }
    enriched["profile_flag"] = flag(enriched)
    return enriched


def summarize(rows: list[dict], key: str) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)

    return [
        {
            key: group,
            "n": len(records),
            "mean_atom_economy": mean(r["atom_economy"] for r in records),
            "mean_e_factor": mean(r["e_factor"] for r in records),
            "mean_pmi": mean(r["process_mass_intensity"] for r in records),
            "mean_hazard_weighted_mass_intensity": mean(r["hazard_weighted_mass_intensity"] for r in records),
            "mean_green_chemistry_score": mean(r["green_chemistry_score"] for r in records),
        }
        for group, records in sorted(groups.items())
    ]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)

    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict]) -> None:
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)
    ranked = sorted(rows, key=lambda r: r["green_chemistry_score"], reverse=True)

    lines = [
        "# Green Chemistry Screening Report",
        "",
        "Synthetic educational screening of green chemistry route metrics.",
        "",
        "## Top routes",
        "",
    ]

    for row in ranked[:5]:
        lines.append(
            f"- {row['route_name']}: score={row['green_chemistry_score']:.3f}, "
            f"AE={row['atom_economy']:.3f}, E-factor={row['e_factor']:.2f}, "
            f"PMI={row['process_mass_intensity']:.2f}, flag={row['profile_flag']}"
        )

    lines.extend([
        "",
        "## Responsible-use note",
        "",
        "These outputs are synthetic and educational. They are not green-chemistry certification, regulatory compliance, life-cycle assessment, toxicity assessment, process-safety validation, or environmental marketing substantiation.",
    ])

    (OUT_REPORTS / "green_chemistry_screening_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(rows: list[dict]) -> None:
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "green-chemistry-responsibility-sustainable-transformation",
        "title": "Green Chemistry, Responsibility, and Sustainable Transformation",
        "records": len(rows),
        "outputs": [
            "outputs/tables/green_chemistry_indicators.csv",
            "outputs/tables/green_chemistry_class_summary.csv",
            "outputs/reports/green_chemistry_screening_report.md",
        ],
        "responsible_use": "Synthetic educational workflow only; not certification, regulatory, LCA, safety, toxicity, or marketing-claim support."
    }
    (OUT_MANIFESTS / "green_chemistry_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    rows = [enrich(row) for row in load_rows()]
    class_summary = summarize(rows, "chemistry_class")

    write_csv(OUT_TABLES / "green_chemistry_indicators.csv", rows)
    write_csv(OUT_TABLES / "green_chemistry_class_summary.csv", class_summary)
    write_report(rows)
    write_manifest(rows)

    print("Green chemistry screening complete.")
    print(f"Routes: {len(rows)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
