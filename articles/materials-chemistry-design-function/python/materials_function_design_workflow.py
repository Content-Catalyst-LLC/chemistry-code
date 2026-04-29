#!/usr/bin/env python3
"""
Synthetic materials chemistry workflow for function-oriented design.

This script demonstrates:
1. Property-vector scoring against a target profile.
2. Weighted objective-function ranking.
3. Sustainability and lifecycle flags.
4. Processing-provenance summaries.
5. Materials-design manifest creation.

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

TARGET_PROFILE = {
    "density_g_cm3": 1.5,
    "modulus_GPa": 10.0,
    "thermal_stability_C": 300.0,
    "conductivity_S_m": 1.0,
    "recyclability_score": 0.85,
    "relative_cost_score": 0.30,
}

WEIGHTS = {
    "density_g_cm3": 1.2,
    "modulus_GPa": 0.8,
    "thermal_stability_C": 1.0,
    "conductivity_S_m": 1.0,
    "recyclability_score": 1.4,
    "relative_cost_score": 1.2,
}

SCALES = {
    "density_g_cm3": 1.0,
    "modulus_GPa": 25.0,
    "thermal_stability_C": 250.0,
    "conductivity_S_m": 10.0,
    "recyclability_score": 0.25,
    "relative_cost_score": 0.30,
}

def objective_score(row: dict[str, str]) -> tuple[float, dict[str, float]]:
    terms: dict[str, float] = {}
    total = 0.0

    for property_name, target_value in TARGET_PROFILE.items():
        observed = float(row[property_name])
        term = WEIGHTS[property_name] * ((observed - target_value) / SCALES[property_name]) ** 2
        terms[property_name] = term
        total += term

    return total, terms

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    materials = read_csv(DATA_DIR / "material_candidates.csv")
    processing = read_csv(DATA_DIR / "processing_conditions.csv")
    properties = read_csv(DATA_DIR / "property_measurements.csv")
    targets = read_csv(DATA_DIR / "function_targets.csv")
    lifecycle = read_csv(DATA_DIR / "lifecycle_notes.csv")

    lifecycle_lookup = {row["material_id"]: row for row in lifecycle}
    processing_lookup = {row["material_id"]: row for row in processing}

    scored_rows = []

    for material in materials:
        score, terms = objective_score(material)
        lifecycle_row = lifecycle_lookup.get(material["material_id"], {})
        processing_row = processing_lookup.get(material["material_id"], {})

        critical_flag = lifecycle_row.get("critical_element_flag", "false").lower() == "true"
        toxicity_flag = lifecycle_row.get("toxicity_flag", "low")
        processing_temperature = float(processing_row.get("processing_temperature_C", 0) or 0)

        responsible_design_flag = (
            critical_flag
            or toxicity_flag in {"medium", "high"}
            or processing_temperature > 1000
        )

        scored_rows.append({
            "material_id": material["material_id"],
            "material_class": material["material_class"],
            "functional_mismatch_score": score,
            "density_term": terms["density_g_cm3"],
            "modulus_term": terms["modulus_GPa"],
            "thermal_stability_term": terms["thermal_stability_C"],
            "conductivity_term": terms["conductivity_S_m"],
            "recyclability_term": terms["recyclability_score"],
            "cost_term": terms["relative_cost_score"],
            "critical_element_flag": critical_flag,
            "toxicity_flag": toxicity_flag,
            "processing_temperature_C": processing_temperature,
            "responsible_design_review_required": responsible_design_flag,
        })

    scored_rows.sort(key=lambda row: row["functional_mismatch_score"])

    for index, row in enumerate(scored_rows, start=1):
        row["rank"] = index

    review_rows = [
        row for row in scored_rows
        if row["responsible_design_review_required"]
    ]

    write_csv(
        TABLE_DIR / "materials_function_screening_ranked.csv",
        scored_rows,
        [
            "material_id",
            "material_class",
            "functional_mismatch_score",
            "density_term",
            "modulus_term",
            "thermal_stability_term",
            "conductivity_term",
            "recyclability_term",
            "cost_term",
            "critical_element_flag",
            "toxicity_flag",
            "processing_temperature_C",
            "responsible_design_review_required",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "materials_responsible_design_review.csv",
        review_rows,
        [
            "material_id",
            "material_class",
            "functional_mismatch_score",
            "critical_element_flag",
            "toxicity_flag",
            "processing_temperature_C",
            "responsible_design_review_required",
            "rank",
        ],
    )

    manifest = {
        "article": "Materials Chemistry and the Design of Function",
        "data_type": "synthetic educational materials chemistry data",
        "target_profile": TARGET_PROFILE,
        "weights": WEIGHTS,
        "scales": SCALES,
        "candidate_count": len(materials),
        "processing_record_count": len(processing),
        "property_measurement_count": len(properties),
        "target_count": len(targets),
        "lifecycle_note_count": len(lifecycle),
        "best_candidate": scored_rows[0]["material_id"],
        "mean_functional_mismatch_score": mean([row["functional_mismatch_score"] for row in scored_rows]),
        "responsible_design_review_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for engineering certification, safety-critical design, or regulatory use.",
    }

    with (MANIFEST_DIR / "materials_design_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "materials_function_design_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Materials Function Design Report\n\n")
        handle.write("Synthetic educational materials chemistry workflow.\n\n")
        handle.write("## Candidate Ranking\n\n")
        for row in scored_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['material_id']} "
                f"({row['material_class']}), score={row['functional_mismatch_score']:.4g}\n"
            )
        handle.write("\n## Responsible Design Review\n\n")
        if review_rows:
            for row in review_rows:
                handle.write(
                    f"- {row['material_id']}: critical={row['critical_element_flag']}, "
                    f"toxicity={row['toxicity_flag']}, "
                    f"processing temperature={row['processing_temperature_C']} C\n"
                )
        else:
            handle.write("- No synthetic candidates flagged for responsible-design review.\n")
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real materials design requires validated measurements, uncertainty analysis, safety review, application testing, and lifecycle evaluation.\n")

    print("Materials function design workflow complete.")

if __name__ == "__main__":
    main()
