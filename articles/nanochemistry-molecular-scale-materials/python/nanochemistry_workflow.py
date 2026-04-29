#!/usr/bin/env python3
"""
Synthetic nanochemistry workflow for molecular-scale materials.

This script demonstrates:
1. Nanoparticle size and hydrodynamic metrics.
2. Surface-area-to-volume scaling.
3. Stokes-Einstein diffusion estimates.
4. Colloidal stability flags.
5. Ligand and lifecycle review integration.
6. Nanochemistry manifest creation.

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

    particles = read_csv(DATA_DIR / "nanomaterial_candidates.csv")
    replicates = read_csv(DATA_DIR / "nanoparticle_replicates.csv")
    ligands = read_csv(DATA_DIR / "ligand_shells.csv")
    optical = read_csv(DATA_DIR / "optical_properties.csv")
    stability_tests = read_csv(DATA_DIR / "stability_media_tests.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")

    ligand_lookup = {row["sample_id"]: row for row in ligands}
    lifecycle_lookup = {row["sample_id"]: row for row in lifecycle}

    k_B = 1.380649e-23
    temperature_K = 298.15
    water_viscosity_Pa_s = 0.00089

    screening_rows = []

    for row in particles:
        core_diameter_nm = float(row["core_diameter_nm"])
        hydro_nm = float(row["hydrodynamic_diameter_nm"])

        surface_area_to_volume_nm_inv = 6.0 / core_diameter_nm
        hydrodynamic_diameter_m = hydro_nm * 1.0e-9

        diffusion_m2_s = (
            k_B * temperature_K
            / (3.0 * math.pi * water_viscosity_Pa_s * hydrodynamic_diameter_m)
        )

        pdi = float(row["polydispersity_index"])
        aggregation = float(row["aggregation_after_salt_relative"])
        zeta = float(row["zeta_potential_mV"])
        ligand_coverage = float(row["ligand_coverage_relative"])
        critical = as_bool(row["critical_material_flag"])

        lifecycle_row = lifecycle_lookup.get(row["sample_id"], {})
        exposure_review = lifecycle_row.get("exposure_review_required", "low")
        ligand_row = ligand_lookup.get(row["sample_id"], {})

        colloidal_review = (
            pdi > 0.25
            or aggregation > 0.30
            or abs(zeta) < 15.0
        )

        responsible_review = (
            critical
            or colloidal_review
            or exposure_review in {"medium", "high"}
        )

        screening_score = (
            1.2 * pdi
            + 1.4 * aggregation
            + 0.8 * (1.0 - ligand_coverage)
            + (0.4 if critical else 0.0)
            + (0.2 if exposure_review == "medium" else 0.0)
            + (0.5 if exposure_review == "high" else 0.0)
        )

        screening_rows.append({
            "sample_id": row["sample_id"],
            "material_class": row["material_class"],
            "core_diameter_nm": core_diameter_nm,
            "hydrodynamic_diameter_nm": hydro_nm,
            "surface_area_to_volume_nm_inv": surface_area_to_volume_nm_inv,
            "diffusion_m2_s": diffusion_m2_s,
            "zeta_potential_mV": zeta,
            "polydispersity_index": pdi,
            "ligand_coverage_relative": ligand_coverage,
            "ligand_class": ligand_row.get("ligand_class", ""),
            "aggregation_after_salt_relative": aggregation,
            "critical_material_flag": critical,
            "exposure_review_required": exposure_review,
            "colloidal_review_required": colloidal_review,
            "responsible_design_review_required": responsible_review,
            "screening_score": screening_score,
        })

    screening_rows.sort(key=lambda item: item["screening_score"])
    for rank, row in enumerate(screening_rows, start=1):
        row["rank"] = rank

    replicate_groups: dict[str, list[dict[str, str]]] = {}
    for row in replicates:
        replicate_groups.setdefault(row["sample_id"], []).append(row)

    replicate_summary = []
    for sample_id, rows in sorted(replicate_groups.items()):
        core_values = [float(row["core_diameter_nm"]) for row in rows]
        hydrodynamic_values = [float(row["hydrodynamic_diameter_nm"]) for row in rows]
        pdi_values = [float(row["polydispersity_index"]) for row in rows]
        aggregation_values = [float(row["aggregation_after_salt_relative"]) for row in rows]

        replicate_summary.append({
            "sample_id": sample_id,
            "mean_core_diameter_nm": mean(core_values),
            "mean_hydrodynamic_diameter_nm": mean(hydrodynamic_values),
            "mean_polydispersity_index": mean(pdi_values),
            "mean_aggregation_after_salt_relative": mean(aggregation_values),
            "replicate_count": len(rows),
        })

    write_csv(
        TABLE_DIR / "nanomaterial_screening_ranked.csv",
        screening_rows,
        [
            "sample_id",
            "material_class",
            "core_diameter_nm",
            "hydrodynamic_diameter_nm",
            "surface_area_to_volume_nm_inv",
            "diffusion_m2_s",
            "zeta_potential_mV",
            "polydispersity_index",
            "ligand_coverage_relative",
            "ligand_class",
            "aggregation_after_salt_relative",
            "critical_material_flag",
            "exposure_review_required",
            "colloidal_review_required",
            "responsible_design_review_required",
            "screening_score",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "nanoparticle_replicate_summary.csv",
        replicate_summary,
        [
            "sample_id",
            "mean_core_diameter_nm",
            "mean_hydrodynamic_diameter_nm",
            "mean_polydispersity_index",
            "mean_aggregation_after_salt_relative",
            "replicate_count",
        ],
    )

    review_rows = [
        row for row in screening_rows
        if row["responsible_design_review_required"]
    ]

    write_csv(
        TABLE_DIR / "nanomaterial_responsible_design_review.csv",
        review_rows,
        [
            "sample_id",
            "material_class",
            "critical_material_flag",
            "exposure_review_required",
            "colloidal_review_required",
            "responsible_design_review_required",
            "rank",
        ],
    )

    manifest = {
        "article": "Nanochemistry and Molecular-Scale Materials",
        "data_type": "synthetic educational nanochemistry data",
        "temperature_K": temperature_K,
        "water_viscosity_Pa_s": water_viscosity_Pa_s,
        "candidate_count": len(particles),
        "replicate_record_count": len(replicates),
        "ligand_record_count": len(ligands),
        "optical_record_count": len(optical),
        "stability_test_count": len(stability_tests),
        "lifecycle_note_count": len(lifecycle),
        "best_candidate": screening_rows[0]["sample_id"],
        "responsible_design_review_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for regulatory, clinical, toxicological, environmental, product-safety, exposure, or nanomedicine decisions.",
    }

    with (MANIFEST_DIR / "nanochemistry_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "nanochemistry_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Nanochemistry Report\n\n")
        handle.write("Synthetic educational nanochemistry workflow.\n\n")
        handle.write("## Candidate Ranking\n\n")
        for row in screening_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['sample_id']} "
                f"({row['material_class']}), score={row['screening_score']:.4g}, "
                f"review={row['responsible_design_review_required']}\n"
            )
        handle.write("\n## Responsible Design Review\n\n")
        for row in review_rows:
            handle.write(
                f"- {row['sample_id']}: critical={row['critical_material_flag']}, "
                f"exposure review={row['exposure_review_required']}, "
                f"colloidal review={row['colloidal_review_required']}\n"
            )
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real nanomaterial characterization requires validated methods, replicate measurements, uncertainty, matrix-specific stability testing, and safety review.\n")

    print("Nanochemistry workflow complete.")

if __name__ == "__main__":
    main()
