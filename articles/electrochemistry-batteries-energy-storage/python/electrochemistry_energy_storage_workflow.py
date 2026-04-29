#!/usr/bin/env python3
"""
Synthetic electrochemistry, batteries, and energy-storage workflow.

This script demonstrates:
1. Battery capacity and energy estimates.
2. Multi-criteria energy-storage candidate screening.
3. Cycling degradation and coulombic-efficiency summaries.
4. Impedance growth and safety/recycling review flags.
5. Lifecycle and responsible-design manifest creation.

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

TARGETS = {
    "cell_energy_Wh": 6.0,
    "cycle_100_capacity_retention": 0.95,
    "coulombic_efficiency": 0.998,
    "rate_capability_score": 0.85,
    "critical_material_score": 0.20,
    "safety_review_score": 0.15,
}

WEIGHTS = {
    "cell_energy_Wh": 0.7,
    "cycle_100_capacity_retention": 1.2,
    "coulombic_efficiency": 1.4,
    "rate_capability_score": 0.9,
    "critical_material_score": 1.3,
    "safety_review_score": 1.1,
}

SCALES = {
    "cell_energy_Wh": 3.0,
    "cycle_100_capacity_retention": 0.08,
    "coulombic_efficiency": 0.008,
    "rate_capability_score": 0.25,
    "critical_material_score": 0.50,
    "safety_review_score": 0.40,
}

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

def linear_slope(x_values: list[float], y_values: list[float]) -> float:
    x_bar = mean(x_values)
    y_bar = mean(y_values)
    numerator = sum((x - x_bar) * (y - y_bar) for x, y in zip(x_values, y_values))
    denominator = sum((x - x_bar) ** 2 for x in x_values)
    return numerator / denominator if denominator else 0.0

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    cells = read_csv(DATA_DIR / "cell_candidates.csv")
    cycling = read_csv(DATA_DIR / "cycling_data.csv")
    voltage_profiles = read_csv(DATA_DIR / "voltage_profiles.csv")
    impedance = read_csv(DATA_DIR / "impedance_measurements.csv")
    materials = read_csv(DATA_DIR / "materials_inventory.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")

    lifecycle_lookup = {row["cell_id"]: row for row in lifecycle}

    screening_rows = []

    for row in cells:
        specific_capacity = float(row["specific_capacity_mAh_g"])
        mass = float(row["active_material_mass_g"])
        voltage = float(row["nominal_voltage_V"])

        cell_capacity_mAh = specific_capacity * mass
        cell_energy_Wh = cell_capacity_mAh * voltage / 1000.0
        cycle_retention = float(row["cycle_100_capacity_retention"])
        coulombic_efficiency = float(row["coulombic_efficiency"])
        rate_score = float(row["rate_capability_score"])
        critical_score = float(row["critical_material_score"])
        safety_score = float(row["safety_review_score"])

        values = {
            "cell_energy_Wh": cell_energy_Wh,
            "cycle_100_capacity_retention": cycle_retention,
            "coulombic_efficiency": coulombic_efficiency,
            "rate_capability_score": rate_score,
            "critical_material_score": critical_score,
            "safety_review_score": safety_score,
        }

        score_terms: dict[str, float] = {}
        screening_score = 0.0
        for property_name, target_value in TARGETS.items():
            term = WEIGHTS[property_name] * ((values[property_name] - target_value) / SCALES[property_name]) ** 2
            score_terms[property_name] = term
            screening_score += term

        lifecycle_row = lifecycle_lookup.get(row["cell_id"], {})

        degradation_review = cycle_retention < 0.90
        efficiency_review = coulombic_efficiency < 0.995
        critical_review = critical_score > 0.60 or as_bool(lifecycle_row.get("critical_material_review", "false"))
        safety_review = safety_score > 0.40 or as_bool(lifecycle_row.get("safety_review_required", "false"))
        responsible_review = as_bool(lifecycle_row.get("responsible_design_review", "false"))

        screening_rows.append({
            "cell_id": row["cell_id"],
            "chemistry": row["chemistry"],
            "nominal_voltage_V": voltage,
            "specific_capacity_mAh_g": specific_capacity,
            "active_material_mass_g": mass,
            "cell_capacity_mAh": cell_capacity_mAh,
            "cell_energy_Wh": cell_energy_Wh,
            "cycle_100_capacity_retention": cycle_retention,
            "coulombic_efficiency": coulombic_efficiency,
            "rate_capability_score": rate_score,
            "critical_material_score": critical_score,
            "safety_review_score": safety_score,
            "cycle_loss_percent_at_100": 100.0 * (1.0 - cycle_retention),
            "estimated_average_capacity_fade_per_cycle_percent": (100.0 * (1.0 - cycle_retention)) / 100.0,
            "degradation_review_required": degradation_review,
            "efficiency_review_required": efficiency_review,
            "critical_material_review_required": critical_review,
            "safety_review_required": safety_review,
            "responsible_design_review_required": responsible_review or degradation_review or efficiency_review or critical_review or safety_review,
            "screening_score": screening_score,
        })

    screening_rows.sort(key=lambda item: item["screening_score"])
    for rank, row in enumerate(screening_rows, start=1):
        row["rank"] = rank

    cycling_groups: dict[str, list[dict[str, str]]] = {}
    for row in cycling:
        cycling_groups.setdefault(row["cell_id"], []).append(row)

    cycling_summary = []
    for cell_id, rows in sorted(cycling_groups.items()):
        sorted_rows = sorted(rows, key=lambda r: float(r["cycle_number"]))
        initial = float(sorted_rows[0]["discharge_capacity_mAh"])
        final = float(sorted_rows[-1]["discharge_capacity_mAh"])
        cycles = [float(row["cycle_number"]) for row in sorted_rows]
        retentions = [float(row["discharge_capacity_mAh"]) / initial for row in sorted_rows]
        efficiencies = [float(row["discharge_capacity_mAh"]) / float(row["charge_capacity_mAh"]) for row in sorted_rows]

        cycling_summary.append({
            "cell_id": cell_id,
            "initial_discharge_capacity_mAh": initial,
            "final_discharge_capacity_mAh": final,
            "final_capacity_retention": final / initial,
            "mean_coulombic_efficiency": mean(efficiencies),
            "retention_slope_per_cycle": linear_slope(cycles, retentions),
            "retention_loss_percent": 100.0 * (1.0 - final / initial),
            "measurement_count": len(rows),
        })

    impedance_groups: dict[str, list[dict[str, str]]] = {}
    for row in impedance:
        impedance_groups.setdefault(row["cell_id"], []).append(row)

    impedance_summary = []
    for cell_id, rows in sorted(impedance_groups.items()):
        sorted_rows = sorted(rows, key=lambda r: float(r["cycle_number"]))
        first = sorted_rows[0]
        last = sorted_rows[-1]

        ohmic_growth = float(last["ohmic_resistance_mOhm"]) - float(first["ohmic_resistance_mOhm"])
        charge_transfer_growth = float(last["charge_transfer_resistance_mOhm"]) - float(first["charge_transfer_resistance_mOhm"])

        impedance_summary.append({
            "cell_id": cell_id,
            "initial_ohmic_resistance_mOhm": float(first["ohmic_resistance_mOhm"]),
            "final_ohmic_resistance_mOhm": float(last["ohmic_resistance_mOhm"]),
            "ohmic_resistance_growth_mOhm": ohmic_growth,
            "initial_charge_transfer_resistance_mOhm": float(first["charge_transfer_resistance_mOhm"]),
            "final_charge_transfer_resistance_mOhm": float(last["charge_transfer_resistance_mOhm"]),
            "charge_transfer_resistance_growth_mOhm": charge_transfer_growth,
            "final_diffusion_tail_score": float(last["diffusion_tail_score"]),
            "impedance_review_required": charge_transfer_growth > 80 or float(last["diffusion_tail_score"]) > 0.75,
        })

    review_rows = [row for row in screening_rows if row["responsible_design_review_required"]]

    write_csv(
        TABLE_DIR / "energy_storage_screening_ranked.csv",
        screening_rows,
        [
            "cell_id",
            "chemistry",
            "nominal_voltage_V",
            "specific_capacity_mAh_g",
            "active_material_mass_g",
            "cell_capacity_mAh",
            "cell_energy_Wh",
            "cycle_100_capacity_retention",
            "coulombic_efficiency",
            "rate_capability_score",
            "critical_material_score",
            "safety_review_score",
            "cycle_loss_percent_at_100",
            "estimated_average_capacity_fade_per_cycle_percent",
            "degradation_review_required",
            "efficiency_review_required",
            "critical_material_review_required",
            "safety_review_required",
            "responsible_design_review_required",
            "screening_score",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "battery_cycling_degradation_summary.csv",
        cycling_summary,
        [
            "cell_id",
            "initial_discharge_capacity_mAh",
            "final_discharge_capacity_mAh",
            "final_capacity_retention",
            "mean_coulombic_efficiency",
            "retention_slope_per_cycle",
            "retention_loss_percent",
            "measurement_count",
        ],
    )

    write_csv(
        TABLE_DIR / "impedance_growth_summary.csv",
        impedance_summary,
        [
            "cell_id",
            "initial_ohmic_resistance_mOhm",
            "final_ohmic_resistance_mOhm",
            "ohmic_resistance_growth_mOhm",
            "initial_charge_transfer_resistance_mOhm",
            "final_charge_transfer_resistance_mOhm",
            "charge_transfer_resistance_growth_mOhm",
            "final_diffusion_tail_score",
            "impedance_review_required",
        ],
    )

    write_csv(
        TABLE_DIR / "responsible_energy_storage_review.csv",
        review_rows,
        [
            "cell_id",
            "chemistry",
            "degradation_review_required",
            "efficiency_review_required",
            "critical_material_review_required",
            "safety_review_required",
            "responsible_design_review_required",
            "rank",
        ],
    )

    manifest = {
        "article": "Electrochemistry, Batteries, and Energy Storage",
        "data_type": "synthetic educational electrochemistry and energy-storage data",
        "target_profile": TARGETS,
        "weights": WEIGHTS,
        "scales": SCALES,
        "candidate_count": len(cells),
        "cycling_record_count": len(cycling),
        "voltage_profile_record_count": len(voltage_profiles),
        "impedance_record_count": len(impedance),
        "materials_record_count": len(materials),
        "lifecycle_note_count": len(lifecycle),
        "best_candidate": screening_rows[0]["cell_id"],
        "responsible_design_review_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for battery design, safety certification, procurement, abuse testing, grid deployment, electric-vehicle use, recycling operations, or regulatory decisions.",
    }

    with (MANIFEST_DIR / "electrochemistry_energy_storage_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "electrochemistry_energy_storage_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Electrochemistry, Batteries, and Energy Storage Report\n\n")
        handle.write("Synthetic educational energy-storage workflow.\n\n")
        handle.write("## Candidate Ranking\n\n")
        for row in screening_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['cell_id']} "
                f"({row['chemistry']}), energy={row['cell_energy_Wh']:.3f} Wh, "
                f"score={row['screening_score']:.4g}, review={row['responsible_design_review_required']}\n"
            )
        handle.write("\n## Cycling Summary\n\n")
        for row in cycling_summary:
            handle.write(
                f"- {row['cell_id']}: final retention={row['final_capacity_retention']:.3f}, "
                f"mean CE={row['mean_coulombic_efficiency']:.5f}, "
                f"loss={row['retention_loss_percent']:.2f}%\n"
            )
        handle.write("\n## Impedance Summary\n\n")
        for row in impedance_summary:
            handle.write(
                f"- {row['cell_id']}: charge-transfer growth="
                f"{row['charge_transfer_resistance_growth_mOhm']:.1f} mOhm, "
                f"review={row['impedance_review_required']}\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real battery claims require validated test protocols, safety testing, aging analysis, abuse testing, manufacturing controls, and lifecycle review.\n")

    print("Electrochemistry energy-storage workflow complete.")

if __name__ == "__main__":
    main()
