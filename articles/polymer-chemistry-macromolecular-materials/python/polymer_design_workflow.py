#!/usr/bin/env python3
"""
Synthetic polymer chemistry workflow for macromolecular materials.

This script demonstrates:
1. Polymer candidate screening against a functional target.
2. Molar-mass average and dispersity calculations.
3. Lifecycle and degradation review flags.
4. Processing-provenance summaries.
5. Polymer-design manifest creation.

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

TARGET_PROFILE = {
    "oxygen_permeability_relative": 0.20,
    "modulus_MPa": 1000.0,
    "elongation_percent": 300.0,
    "recyclability_score": 0.80,
    "relative_cost_score": 0.30,
}

WEIGHTS = {
    "oxygen_permeability_relative": 1.6,
    "modulus_MPa": 0.8,
    "elongation_percent": 1.0,
    "recyclability_score": 1.3,
    "relative_cost_score": 1.0,
}

SCALES = {
    "oxygen_permeability_relative": 0.50,
    "modulus_MPa": 1000.0,
    "elongation_percent": 250.0,
    "recyclability_score": 0.25,
    "relative_cost_score": 0.30,
}

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def objective_score(row: dict[str, str]) -> tuple[float, dict[str, float]]:
    terms: dict[str, float] = {}
    total = 0.0

    for property_name, target_value in TARGET_PROFILE.items():
        observed = float(row[property_name])
        term = WEIGHTS[property_name] * ((observed - target_value) / SCALES[property_name]) ** 2
        terms[property_name] = term
        total += term

    return total, terms

def molar_mass_summary(rows: list[dict[str, str]]) -> dict[str, float]:
    counts = [float(row["molecule_count"]) for row in rows]
    masses = [float(row["molar_mass_g_mol"]) for row in rows]

    mn = sum(n * m for n, m in zip(counts, masses)) / sum(counts)
    mw = sum(n * m * m for n, m in zip(counts, masses)) / sum(n * m for n, m in zip(counts, masses))
    dispersity = mw / mn

    return {
        "Mn_g_mol": mn,
        "Mw_g_mol": mw,
        "dispersity": dispersity,
    }

def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    polymers = read_csv(DATA_DIR / "polymer_candidates.csv")
    fractions = read_csv(DATA_DIR / "molar_mass_fractions.csv")
    processing = read_csv(DATA_DIR / "processing_conditions.csv")
    measurements = read_csv(DATA_DIR / "property_measurements.csv")
    lifecycle = read_csv(DATA_DIR / "degradation_lifecycle_notes.csv")
    targets = read_csv(DATA_DIR / "function_targets.csv")

    lifecycle_lookup = {row["polymer_id"]: row for row in lifecycle}
    processing_lookup = {row["polymer_id"]: row for row in processing}

    fraction_groups: dict[str, list[dict[str, str]]] = {}
    for row in fractions:
        fraction_groups.setdefault(row["polymer_id"], []).append(row)

    molar_rows = []
    for polymer_id, group in sorted(fraction_groups.items()):
        summary = molar_mass_summary(group)
        molar_rows.append({
            "polymer_id": polymer_id,
            **summary,
        })

    scored_rows = []

    for polymer in polymers:
        score, terms = objective_score(polymer)
        lifecycle_row = lifecycle_lookup.get(polymer["polymer_id"], {})
        processing_row = processing_lookup.get(polymer["polymer_id"], {})

        biodegradation_status = lifecycle_row.get("biodegradation_claim_status", "")
        recycling_pathway = lifecycle_row.get("recycling_pathway", "")
        processing_temperature = float(processing_row.get("processing_temperature_C", 0) or 0)

        responsible_review = (
            recycling_pathway in {"difficult_network_recycling", "specialized_recycling"}
            or biodegradation_status.startswith("conditional")
            or processing_temperature > 300
        )

        scored_rows.append({
            "polymer_id": polymer["polymer_id"],
            "polymer_class": polymer["polymer_class"],
            "functional_mismatch_score": score,
            "oxygen_permeability_term": terms["oxygen_permeability_relative"],
            "modulus_term": terms["modulus_MPa"],
            "elongation_term": terms["elongation_percent"],
            "recyclability_term": terms["recyclability_score"],
            "cost_term": terms["relative_cost_score"],
            "recycling_pathway": recycling_pathway,
            "biodegradation_claim_status": biodegradation_status,
            "processing_temperature_C": processing_temperature,
            "responsible_design_review_required": responsible_review,
        })

    scored_rows.sort(key=lambda row: row["functional_mismatch_score"])

    for index, row in enumerate(scored_rows, start=1):
        row["rank"] = index

    review_rows = [
        row for row in scored_rows
        if row["responsible_design_review_required"]
    ]

    write_csv(
        TABLE_DIR / "polymer_candidate_screening_ranked.csv",
        scored_rows,
        [
            "polymer_id",
            "polymer_class",
            "functional_mismatch_score",
            "oxygen_permeability_term",
            "modulus_term",
            "elongation_term",
            "recyclability_term",
            "cost_term",
            "recycling_pathway",
            "biodegradation_claim_status",
            "processing_temperature_C",
            "responsible_design_review_required",
            "rank",
        ],
    )

    write_csv(
        TABLE_DIR / "polymer_molar_mass_summary.csv",
        molar_rows,
        ["polymer_id", "Mn_g_mol", "Mw_g_mol", "dispersity"],
    )

    write_csv(
        TABLE_DIR / "polymer_responsible_design_review.csv",
        review_rows,
        [
            "polymer_id",
            "polymer_class",
            "functional_mismatch_score",
            "recycling_pathway",
            "biodegradation_claim_status",
            "processing_temperature_C",
            "responsible_design_review_required",
            "rank",
        ],
    )

    manifest = {
        "article": "Polymer Chemistry and Macromolecular Materials",
        "data_type": "synthetic educational polymer chemistry data",
        "target_profile": TARGET_PROFILE,
        "weights": WEIGHTS,
        "scales": SCALES,
        "candidate_count": len(polymers),
        "molar_mass_fraction_count": len(fractions),
        "processing_record_count": len(processing),
        "property_measurement_count": len(measurements),
        "lifecycle_note_count": len(lifecycle),
        "target_count": len(targets),
        "best_candidate": scored_rows[0]["polymer_id"],
        "mean_functional_mismatch_score": mean([row["functional_mismatch_score"] for row in scored_rows]),
        "responsible_design_review_count": len(review_rows),
        "responsible_use": "Synthetic educational data only; not validated for engineering certification, biodegradation claims, recycling claims, or regulated polymer use.",
    }

    with (MANIFEST_DIR / "polymer_design_manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    with (REPORT_DIR / "polymer_design_report.md").open("w", encoding="utf-8") as handle:
        handle.write("# Polymer Design Report\n\n")
        handle.write("Synthetic educational polymer chemistry workflow.\n\n")
        handle.write("## Candidate Ranking\n\n")
        for row in scored_rows:
            handle.write(
                f"- Rank {row['rank']}: {row['polymer_id']} "
                f"({row['polymer_class']}), score={row['functional_mismatch_score']:.4g}\n"
            )
        handle.write("\n## Molar-Mass Summary\n\n")
        for row in molar_rows:
            handle.write(
                f"- {row['polymer_id']}: Mn={row['Mn_g_mol']:.4g} g/mol, "
                f"Mw={row['Mw_g_mol']:.4g} g/mol, dispersity={row['dispersity']:.4g}\n"
            )
        handle.write("\n## Responsible Design Review\n\n")
        if review_rows:
            for row in review_rows:
                handle.write(
                    f"- {row['polymer_id']}: recycling pathway={row['recycling_pathway']}, "
                    f"biodegradation status={row['biodegradation_claim_status']}, "
                    f"processing temperature={row['processing_temperature_C']} C\n"
                )
        else:
            handle.write("- No synthetic candidates flagged for responsible-design review.\n")
        handle.write("\n## Responsible-Use Note\n\n")
        handle.write("Synthetic educational data only. Real polymer decisions require validated characterization, processing trials, aging studies, safety review, and lifecycle evaluation.\n")

    print("Polymer chemistry workflow complete.")

if __name__ == "__main__":
    main()
