#!/usr/bin/env python3
"""
Synthetic colloid, soft matter, and complex-fluid workflow.

This script demonstrates:
1. Colloidal diffusion estimates.
2. Volume-fraction and rheology screening.
3. Shear-thinning and yield-stress flags.
4. Stability and aggregation review.
5. Lifecycle and responsible formulation review.
6. Colloid soft-matter manifest creation.

The data are synthetic and educational only.
"""

from __future__ import annotations

import csv
import json
import math
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

    systems = read_csv(DATA_DIR / "colloid_systems.csv")
    replicates = read_csv(DATA_DIR / "rheology_replicates.csv")
    stability_tests = read_csv(DATA_DIR / "stability_tests.csv")
    emulsions = read_csv(DATA_DIR / "emulsion_properties.csv")
    gels = read_csv(DATA_DIR / "gel_networks.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")

    lifecycle_lookup = {row["formulation_id"]: row for row in lifecycle}

    k_B = 1.380649e-23
    temperature_K = 298.15
    continuous_phase_viscosity_Pa_s = 0.00089

    screening_rows = []

    for row in systems:
        diameter_nm = float(row["particle_or_droplet_size_nm"])
        diameter_m = diameter_nm * 1.0e-9

        diffusion = (
            k_B * temperature_K
            / (3.0 * math.pi * continuous_phase_viscosity_Pa_s * diameter_m)
        )

        volume_fraction = float(row["volume_fraction"])
        low_visc = float(row["low_shear_viscosity_Pa_s"])
        high_visc = float(row["high_shear_viscosity_Pa_s"])
        yield_stress = float(row["yield_stress_Pa"])
        salt_aggregation = float(row["salt_aggregation_index"])
        zeta = float(row["zeta_potential_mV"])

        shear_thinning_ratio = low_visc / high_visc if high_visc > 0 else float("inf")
        electrostatic_review = abs(zeta) < 20.0
        aggregation_review = salt_aggregation > 0.30
        yield_stress_review = yield_stress > 10.0
        crowding_review = volume_fraction > 0.25

        lifecycle_row = lifecycle_lookup.get(row["formulation_id"], {})
        responsible_review = as_bool(lifecycle_row.get("responsible_formulation_review", "false"))

        formulation_review_required = (
            electrostatic_review
            or aggregation_review
            or yield_stress_review
            or crowding_review
            or responsible_review
        )

        screening_score = (
            1.2 * salt_aggregation
            + 0.8 * volume_fraction
            + 0.01 * yield_stress
            + (0.25 if electrostatic_review else 0.0)
            + (0.30 if responsible_review else 0.0)
        )

        screening_rows.append({
            "formulation_id": row["formulation_id"],
            "system_type": row["system_type"],
            "dispersed_phase": row["dispersed_phase"],
            "continuous_phase": row["continuous_phase"],
            "particle_or_droplet_size_nm": diameter_nm,
            "zeta_potential_mV": zeta,
            "volume_fraction": volume_fraction,
            "low_shear_viscosity_Pa_s": low_visc,
            "high_shear_viscosity_Pa_s": high_visc,
            "yield_stress_Pa": yield_stress,
            "salt_aggregation_index": salt_aggregation,
            "diffusion_m2_s": diffusion,
            "shear_thinning_ratio": shear_thinning_ratio,
            "electrostatic_stability_review": electrostatic_review,
            "aggregation_review": aggregation_review,
            "yield_stress_review": yield_stress_review,
            "high_crowding_review": crowding_review,
            "responsible_formulation_review": responsible_review,
            "formulation_review_required": formulation_review_required,
            "screening_score": screening_score,
        })

    screening_rows.sort(key=lambda row: row["screening_score"])
    for index, row in enumerate(screening_rows, start=1):
        row["rank"] = index

    replicate_groups: dict[str, list[dict[str, str]]] = {}
    for row in replicates:
        replicate_groups.setdefault(row["formulation_id"], []).append(row)

    replicate_summary = []
    for formulation_id, rows in sorted(replicate_groups.items()):
        low_values = [float(row["low_shear_viscosity_Pa_s"]) for row in rows]
        high_values = [float(row["high_shear_viscosity_Pa_s"]) for row in rows]
        yield_values = [float(row["yield_stress_Pa"]) for row in rows]
        aggregation_values = [float(row["salt_aggregation_index"]) for row in rows]

        mean_low = mean(low_values)
        mean_high = mean(high_values)
        replicate_summary.append({
            "formulation_id": formulation_id,
            "mean_low_shear_viscosity_Pa_s": mean_low,
            "mean_high_shear_viscosity_Pa_s": mean_high,
            "mean_yield_stress_Pa": mean(yield_values),
            "mean_salt_aggregation_index": mean(aggregation_values),
            "shear_thinning_ratio": mean_low / mean_high if mean_high > 0 else "",
            "replicate_count": len(rows),
        })

    stability_flags = [
        row for row in stability_tests
        if as_bool(row["aggregation_flag"])
        or float(row["phase_separation_index"]) > 0.20
        or float(row["sedimentation_index"]) > 0.20
        or float(row["creaming_index"]) > 0.20
    ]

    review_rows = [
        row for row in screening_rows
        if row["formulation_review_required"]
    ]

    write_csv(
        TABLE_DIR / "colloid_complex_fluid_screening_ranked.csv",
        screening_rows,
        [
            "formulation_id",
            "system_type",
            "dispersed_phase",
            "continuous_phase",
            "particle_or_droplet_size_nm",
            "zeta_potential_mV",
            "volume_fraction",
            "low_shear_viscosity_Pa_s",
            "high_shear_viscosity_Pa_s",
            "yield_stress_Pa",
            "salt_aggregation_index",
            "diffusion_m2_s",
            "shear_thinning_ratio",
            "electrostatic_stability_review",
            "aggregation_review",
            "yield_stress_review",
            "high_crowding_review",
            "responsible_formulation_review",
            "formulation_review_required",
            "screening_score",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "rheology_replicate_summary.csv",
        replicate_summary,
        [
            "formulation_id",
            "mean_low_shear_viscosity_Pa_s",
            "mean_high_shear_viscosity_Pa_s",
            "mean_yield_stress_Pa",
            "mean_salt_aggregation_index",
            "shear_thinning_ratio",
            "replicate_count",
        ],
    )

    write_csv(
        TABLE_DIR / "stability_review_flags.csv",
        stability_flags,
        [
            "test_id",
            "formulation_id",
            "condition",
            "temperature_C",
            "storage_days",
            "phase_separation_index",
            "sedimentation_index",
            "creaming_index",
            "aggregation_flag",
        ],
    )

    write_csv(
        TABLE_DIR / "responsible_formulation_review.csv",
        review_rows,
        [
            "formulation_id",
            "system_type",
            "formulation_review_required",
            "responsible_formulation_review",
            "aggregation_review",
            "yield_stress_review",
            "high_crowding_review",
            "rank",
        ],
    )

    manifest = {
        "article": "Colloids, Soft Matter, and Complex Fluids",
        "data_type": "synthetic educational colloid and complex-fluid data",
        "temperature_K": temperature_K,
        "continuous_phase_viscosity_Pa_s": continuous_phase_viscosity_Pa_s,
        "system_count": len(systems),
        "replicate_record_count": len(replicates),
        "stability_test_count": len(stability_tests),
        "emulsion_record_count": len(emulsions),
        "gel_record_count": len(gels),
        "lifecycle_note_count": len(lifecycle),
        "best_candidate": screening_rows[0]["formulation_id"],
        "stability_flag_count": len(stability_flags),
        "review_required_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for product qualification, food safety, medical use, environmental claims, industrial process control, cosmetics claims, or regulatory decisions.",
    }

    with (MANIFEST_DIR / "colloid_soft_matter_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "colloid_soft_matter_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Colloid Soft Matter Report\n\n")
        handle.write("Synthetic educational colloids, soft matter, and complex fluids workflow.\n\n")
        handle.write("## Candidate Ranking\n\n")
        for row in screening_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['formulation_id']} "
                f"({row['system_type']}), score={row['screening_score']:.4g}, "
                f"review={row['formulation_review_required']}\n"
            )
        handle.write("\n## Stability Flags\n\n")
        if stability_flags:
            for row in stability_flags:
                handle.write(
                    f"- {row['formulation_id']} under {row['condition']}: "
                    f"aggregation={row['aggregation_flag']}, "
                    f"phase separation={row['phase_separation_index']}\n"
                )
        else:
            handle.write("- No synthetic stability flags.\n")
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real colloid and complex-fluid evaluation requires validated particle-size, stability, rheology, aging, and application-specific testing.\n")

    print("Colloid soft matter workflow complete.")

if __name__ == "__main__":
    main()
