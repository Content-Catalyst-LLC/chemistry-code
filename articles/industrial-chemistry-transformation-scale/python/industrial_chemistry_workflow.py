#!/usr/bin/env python3
"""
Synthetic industrial chemistry and scale-up workflow.

This script demonstrates:
1. Industrial route screening.
2. Yield, E-factor, solvent intensity, energy intensity, and space-time yield.
3. Scale-up, hazard, separation, waste, and energy review flags.
4. Unit-operation and decarbonization summaries.
5. Responsible-scale manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
TABLE_DIR = BASE_DIR / "outputs" / "tables"
REPORT_DIR = BASE_DIR / "outputs" / "reports"
MANIFEST_DIR = BASE_DIR / "outputs" / "manifests"

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def as_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    routes = read_csv(DATA_DIR / "process_routes.csv")
    batches = read_csv(DATA_DIR / "batch_data.csv")
    unit_operations = read_csv(DATA_DIR / "unit_operations.csv")
    hazards = read_csv(DATA_DIR / "hazard_register.csv")
    decarb = read_csv(DATA_DIR / "decarbonization_pathways.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")

    lifecycle_lookup = {row["route_id"]: row for row in lifecycle}

    screening_rows = []

    for row in routes:
        actual_product = float(row["actual_product_kg"])
        theoretical_product = float(row["theoretical_product_kg"])
        waste_kg = float(row["waste_kg"])
        solvent_kg = float(row["solvent_kg"])
        energy_kWh = float(row["energy_kWh"])
        reactor_volume = float(row["reactor_volume_m3"])
        time_h = float(row["batch_or_residence_time_h"])
        hazard_score = float(row["hazard_score"])
        separation_score = float(row["separation_difficulty_score"])
        feedstock_risk = float(row["feedstock_risk_score"])

        yield_fraction = actual_product / theoretical_product
        e_factor = waste_kg / actual_product
        solvent_intensity = solvent_kg / actual_product
        energy_intensity = energy_kWh / actual_product
        space_time_yield = actual_product / (reactor_volume * time_h)

        waste_review = e_factor > 1.0
        solvent_review = solvent_intensity > 2.0
        energy_review = energy_intensity > 3.0
        hazard_review = hazard_score > 0.60
        separation_review = separation_score > 0.70

        lifecycle_row = lifecycle_lookup.get(row["route_id"], {})
        responsible_scale_review = as_bool(lifecycle_row.get("responsible_scale_review", "false"))

        scale_up_review = (
            waste_review
            or solvent_review
            or energy_review
            or hazard_review
            or separation_review
            or responsible_scale_review
        )

        screening_score = (
            1.5 * (1.0 - yield_fraction)
            + 1.2 * e_factor
            + 0.7 * solvent_intensity
            + 0.5 * energy_intensity
            + 1.4 * hazard_score
            + 1.0 * separation_score
            + 0.6 * feedstock_risk
            - 0.04 * space_time_yield
        )

        screening_rows.append({
            "route_id": row["route_id"],
            "process_type": row["process_type"],
            "yield_fraction": yield_fraction,
            "e_factor": e_factor,
            "solvent_intensity": solvent_intensity,
            "energy_intensity_kWh_kg": energy_intensity,
            "space_time_yield_kg_m3_h": space_time_yield,
            "hazard_score": hazard_score,
            "separation_difficulty_score": separation_score,
            "feedstock_risk_score": feedstock_risk,
            "waste_review_required": waste_review,
            "solvent_review_required": solvent_review,
            "energy_review_required": energy_review,
            "hazard_review_required": hazard_review,
            "separation_review_required": separation_review,
            "responsible_scale_review": responsible_scale_review,
            "scale_up_review_required": scale_up_review,
            "screening_score": screening_score,
        })

    screening_rows.sort(key=lambda row: row["screening_score"])
    for rank, row in enumerate(screening_rows, start=1):
        row["rank"] = rank

    operation_groups: dict[str, list[dict[str, str]]] = {}
    for row in unit_operations:
        operation_groups.setdefault(row["route_id"], []).append(row)

    unit_operation_summary = []
    for route_id, rows in sorted(operation_groups.items()):
        total_energy = sum(float(row["energy_kWh"]) for row in rows)
        total_water = sum(float(row["water_m3"]) for row in rows)
        total_solvent_loss = sum(float(row["solvent_loss_kg"]) for row in rows)
        quality_critical_count = sum(as_bool(row["quality_critical_flag"]) for row in rows)

        unit_operation_summary.append({
            "route_id": route_id,
            "operation_count": len(rows),
            "total_operation_energy_kWh": total_energy,
            "total_water_m3": total_water,
            "total_solvent_loss_kg": total_solvent_loss,
            "quality_critical_operation_count": quality_critical_count,
        })

    hazard_rows = []
    for row in hazards:
        severity = float(row["severity_score"])
        likelihood = float(row["likelihood_score"])
        safeguard = float(row["safeguard_score"])
        residual_risk_proxy = severity * likelihood * (1.0 - safeguard)

        hazard_rows.append({
            "hazard_id": row["hazard_id"],
            "route_id": row["route_id"],
            "hazard_type": row["hazard_type"],
            "severity_score": severity,
            "likelihood_score": likelihood,
            "safeguard_score": safeguard,
            "residual_risk_proxy": residual_risk_proxy,
            "review_required": as_bool(row["review_required"]),
        })

    decarb_rows = []
    for row in decarb:
        energy_reduction = float(row["energy_reduction_percent"])
        emissions_reduction = float(row["emissions_reduction_percent"])
        implementation = float(row["implementation_difficulty_score"])
        capital = float(row["capital_intensity_score"])

        decarb_priority_score = (
            0.45 * energy_reduction
            + 0.55 * emissions_reduction
            - 10.0 * implementation
            - 6.0 * capital
        )

        decarb_rows.append({
            "pathway_id": row["pathway_id"],
            "route_id": row["route_id"],
            "pathway": row["pathway"],
            "energy_reduction_percent": energy_reduction,
            "emissions_reduction_percent": emissions_reduction,
            "implementation_difficulty_score": implementation,
            "capital_intensity_score": capital,
            "decarbonization_priority_score": decarb_priority_score,
        })

    decarb_rows.sort(key=lambda row: row["decarbonization_priority_score"], reverse=True)

    review_rows = [row for row in screening_rows if row["scale_up_review_required"]]

    write_csv(
        TABLE_DIR / "industrial_process_screening_ranked.csv",
        screening_rows,
        [
            "route_id",
            "process_type",
            "yield_fraction",
            "e_factor",
            "solvent_intensity",
            "energy_intensity_kWh_kg",
            "space_time_yield_kg_m3_h",
            "hazard_score",
            "separation_difficulty_score",
            "feedstock_risk_score",
            "waste_review_required",
            "solvent_review_required",
            "energy_review_required",
            "hazard_review_required",
            "separation_review_required",
            "responsible_scale_review",
            "scale_up_review_required",
            "screening_score",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "unit_operation_summary.csv",
        unit_operation_summary,
        [
            "route_id",
            "operation_count",
            "total_operation_energy_kWh",
            "total_water_m3",
            "total_solvent_loss_kg",
            "quality_critical_operation_count",
        ],
    )

    write_csv(
        TABLE_DIR / "hazard_register_risk_proxy.csv",
        hazard_rows,
        [
            "hazard_id",
            "route_id",
            "hazard_type",
            "severity_score",
            "likelihood_score",
            "safeguard_score",
            "residual_risk_proxy",
            "review_required",
        ],
    )

    write_csv(
        TABLE_DIR / "decarbonization_pathway_priority.csv",
        decarb_rows,
        [
            "pathway_id",
            "route_id",
            "pathway",
            "energy_reduction_percent",
            "emissions_reduction_percent",
            "implementation_difficulty_score",
            "capital_intensity_score",
            "decarbonization_priority_score",
        ],
    )

    write_csv(
        TABLE_DIR / "scale_up_review_routes.csv",
        review_rows,
        [
            "route_id",
            "process_type",
            "waste_review_required",
            "solvent_review_required",
            "energy_review_required",
            "hazard_review_required",
            "separation_review_required",
            "responsible_scale_review",
            "scale_up_review_required",
            "rank",
        ],
    )

    manifest = {
        "article": "Industrial Chemistry and the Transformation of Scale",
        "data_type": "synthetic educational industrial chemistry data",
        "route_count": len(routes),
        "batch_record_count": len(batches),
        "unit_operation_record_count": len(unit_operations),
        "hazard_record_count": len(hazards),
        "decarbonization_record_count": len(decarb),
        "lifecycle_note_count": len(lifecycle),
        "best_candidate": screening_rows[0]["route_id"],
        "scale_up_review_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for plant design, process safety, process control, regulatory reporting, GMP release, environmental claims, procurement, or industrial investment decisions.",
    }

    with (MANIFEST_DIR / "industrial_chemistry_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "industrial_chemistry_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Industrial Chemistry and Scale-Up Report\n\n")
        handle.write("Synthetic educational industrial chemistry workflow.\n\n")
        handle.write("## Route Ranking\n\n")
        for row in screening_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['route_id']} "
                f"({row['process_type']}), yield={row['yield_fraction']:.3f}, "
                f"E-factor={row['e_factor']:.3f}, score={row['screening_score']:.4g}, "
                f"review={row['scale_up_review_required']}\n"
            )
        handle.write("\n## Highest Priority Decarbonization Pathways\n\n")
        for row in decarb_rows[:5]:
            handle.write(
                f"- {row['route_id']} / {row['pathway']}: "
                f"energy reduction={row['energy_reduction_percent']:.1f}%, "
                f"emissions reduction={row['emissions_reduction_percent']:.1f}%, "
                f"priority={row['decarbonization_priority_score']:.3f}\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real process development requires validated chemistry, thermochemistry, hazard studies, process safety review, equipment design, environmental assessment, quality systems, and economic analysis.\n")

    print("Industrial chemistry workflow complete.")

if __name__ == "__main__":
    main()
