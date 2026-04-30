#!/usr/bin/env python3
"""
Circular Chemistry, Waste, and Material Futures

Synthetic educational workflow for circular chemistry:
- recovery yield
- circular retention
- material loss over cycles
- hazard-weighted recovered flow
- energy intensity
- reagent intensity
- collection and sorting performance
- traceability and contamination
- critical-material recovery context
- composite circular chemistry score

Not a recycling certification, waste-management, LCA, regulatory,
toxicology, product-claim, or food-contact suitability tool.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "circular_chemistry_full_stack_synthetic.csv"
OUT_TABLES = ROOT / "outputs" / "tables"
OUT_REPORTS = ROOT / "outputs" / "reports"
OUT_MANIFESTS = ROOT / "outputs" / "manifests"

NUMERIC = {
    "input_waste_kg",
    "recovered_useful_kg",
    "recovered_quality_factor",
    "substitution_factor",
    "energy_kwh",
    "solvent_or_reagent_kg",
    "process_water_kg",
    "hazard_score",
    "exposure_relevance",
    "contamination_score",
    "traceability_score",
    "collection_rate",
    "sorting_efficiency",
    "reuse_cycles",
    "loss_fraction_per_cycle",
    "critical_material_fraction",
    "worker_exposure_score",
    "qc_score",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def parse_row(row: dict) -> dict:
    parsed = {}
    for key, value in row.items():
        parsed[key] = float(value) if key in NUMERIC else value
    return parsed


def load_rows() -> list[dict]:
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        return [parse_row(row) for row in csv.DictReader(handle)]


def recovery_yield(row: dict) -> float:
    if row["input_waste_kg"] <= 0:
        return 0.0
    return row["recovered_useful_kg"] / row["input_waste_kg"]


def circular_retention(row: dict) -> float:
    return recovery_yield(row) * row["recovered_quality_factor"] * row["substitution_factor"]


def material_remaining_after_cycles(row: dict) -> float:
    return row["input_waste_kg"] * ((1.0 - row["loss_fraction_per_cycle"]) ** row["reuse_cycles"])


def hazard_weighted_recovered_flow(row: dict) -> float:
    return row["recovered_useful_kg"] * row["hazard_score"] * row["exposure_relevance"]


def energy_intensity(row: dict) -> float:
    if row["recovered_useful_kg"] <= 0:
        return 0.0
    return row["energy_kwh"] / row["recovered_useful_kg"]


def reagent_intensity(row: dict) -> float:
    if row["recovered_useful_kg"] <= 0:
        return 0.0
    return row["solvent_or_reagent_kg"] / row["recovered_useful_kg"]


def water_intensity(row: dict) -> float:
    if row["recovered_useful_kg"] <= 0:
        return 0.0
    return row["process_water_kg"] / row["recovered_useful_kg"]


def infrastructure_score(row: dict) -> float:
    return clamp(
        0.45 * row["collection_rate"] +
        0.40 * row["sorting_efficiency"] +
        0.15 * row["traceability_score"]
    )


def safe_circularity_score(row: dict) -> float:
    hazard_component = 1.0 - row["hazard_score"]
    exposure_component = 1.0 - row["exposure_relevance"]
    contamination_component = 1.0 - row["contamination_score"]
    worker_component = 1.0 - row["worker_exposure_score"]
    return clamp(
        0.30 * hazard_component +
        0.25 * exposure_component +
        0.25 * contamination_component +
        0.20 * worker_component
    )


def circular_chemistry_score(row: dict) -> float:
    recovery = recovery_yield(row)
    retention = circular_retention(row)
    infrastructure = infrastructure_score(row)
    safety = safe_circularity_score(row)
    energy_score = clamp(1.0 - energy_intensity(row) / 2.0)
    reagent_score = clamp(1.0 - reagent_intensity(row) / 0.6)
    water_score = clamp(1.0 - water_intensity(row) / 1.0)
    critical_value = clamp(row["critical_material_fraction"] * row["substitution_factor"])
    traceability = row["traceability_score"]
    qc = row["qc_score"]

    return clamp(
        0.16 * recovery +
        0.18 * retention +
        0.13 * infrastructure +
        0.15 * safety +
        0.10 * energy_score +
        0.08 * reagent_score +
        0.06 * water_score +
        0.06 * critical_value +
        0.05 * traceability +
        0.03 * qc
    )


def flag(row: dict) -> str:
    score = row["circular_chemistry_score"]
    if score >= 0.70:
        return "strong_circular_profile"
    if score >= 0.50:
        return "moderate_profile_with_constraints"
    return "redesign_or_infrastructure_priority"


def enrich(row: dict) -> dict:
    enriched = {
        **row,
        "recovery_yield": recovery_yield(row),
        "circular_retention": circular_retention(row),
        "material_remaining_after_cycles_kg": material_remaining_after_cycles(row),
        "hazard_weighted_recovered_flow": hazard_weighted_recovered_flow(row),
        "energy_intensity_kwh_per_kg_recovered": energy_intensity(row),
        "reagent_intensity_kg_per_kg_recovered": reagent_intensity(row),
        "water_intensity_kg_per_kg_recovered": water_intensity(row),
        "infrastructure_score": infrastructure_score(row),
        "safe_circularity_score": safe_circularity_score(row),
        "circular_chemistry_score": circular_chemistry_score(row),
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
            "mean_recovery_yield": mean(r["recovery_yield"] for r in records),
            "mean_circular_retention": mean(r["circular_retention"] for r in records),
            "mean_hazard_weighted_recovered_flow": mean(r["hazard_weighted_recovered_flow"] for r in records),
            "mean_safe_circularity_score": mean(r["safe_circularity_score"] for r in records),
            "mean_circular_chemistry_score": mean(r["circular_chemistry_score"] for r in records),
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
    ranked = sorted(rows, key=lambda r: r["circular_chemistry_score"], reverse=True)

    lines = [
        "# Circular Chemistry Screening Report",
        "",
        "Synthetic educational screening of circular material-system metrics.",
        "",
        "## Top streams",
        "",
    ]

    for row in ranked[:5]:
        lines.append(
            f"- {row['material_stream']}: score={row['circular_chemistry_score']:.3f}, "
            f"recovery={row['recovery_yield']:.3f}, retention={row['circular_retention']:.3f}, "
            f"safe circularity={row['safe_circularity_score']:.3f}, flag={row['profile_flag']}"
        )

    lines.extend([
        "",
        "## Responsible-use note",
        "",
        "These outputs are synthetic and educational. They are not recyclability certification, regulatory compliance, life-cycle assessment, waste-management approval, toxicology review, food-contact suitability assessment, or product-claim substantiation.",
    ])

    (OUT_REPORTS / "circular_chemistry_screening_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(rows: list[dict]) -> None:
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)
    manifest = {
        "article_slug": "circular-chemistry-waste-material-futures",
        "title": "Circular Chemistry, Waste, and Material Futures",
        "records": len(rows),
        "outputs": [
            "outputs/tables/circular_chemistry_indicators.csv",
            "outputs/tables/circular_chemistry_material_class_summary.csv",
            "outputs/tables/circular_chemistry_pathway_summary.csv",
            "outputs/reports/circular_chemistry_screening_report.md"
        ],
        "responsible_use": "Synthetic educational workflow only; not certification, regulatory, LCA, recycling validation, toxicity, food-contact, or product-claim support."
    }
    (OUT_MANIFESTS / "circular_chemistry_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    rows = [enrich(row) for row in load_rows()]

    write_csv(OUT_TABLES / "circular_chemistry_indicators.csv", rows)
    write_csv(OUT_TABLES / "circular_chemistry_material_class_summary.csv", summarize(rows, "material_class"))
    write_csv(OUT_TABLES / "circular_chemistry_pathway_summary.csv", summarize(rows, "recovery_pathway"))
    write_report(rows)
    write_manifest(rows)

    print("Circular chemistry screening complete.")
    print(f"Material streams: {len(rows)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
