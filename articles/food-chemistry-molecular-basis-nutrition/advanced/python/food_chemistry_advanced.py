#!/usr/bin/env python3
"""
Advanced food chemistry and nutrition workflow.

Article:
Food Chemistry and the Molecular Basis of Nutrition

This script uses synthetic food chemistry records to calculate:

- nutrient-density proxies
- bioavailability-adjusted nutrients
- food-matrix accessibility
- protein quality and digestibility screens
- glycemic accessibility proxy
- lipid oxidation vulnerability
- vitamin retention scenarios
- mineral bioavailability scenarios
- processing and matrix effect scenarios
- food-safety and sodium flags
- sustainability context summaries
- SQL-ready provenance outputs

This is educational scaffolding only. It is not dietary advice, clinical
nutrition guidance, food-safety certification, allergen clearance, regulatory
compliance, product health-claim support, or a substitute for qualified
professional review.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ADV_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ADV_DIR / "data" / "food_chemistry_advanced_synthetic.csv"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"

NUMERIC_FIELDS = {
    "energy_kcal",
    "water_g",
    "protein_g",
    "total_carbohydrate_g",
    "digestible_starch_g",
    "total_sugars_g",
    "fiber_g",
    "total_fat_g",
    "saturated_fat_g",
    "monounsaturated_fat_g",
    "polyunsaturated_fat_g",
    "omega3_g",
    "iron_mg",
    "zinc_mg",
    "calcium_mg",
    "potassium_mg",
    "vitamin_c_mg",
    "folate_ug",
    "polyphenol_mg",
    "water_activity",
    "pH",
    "particle_accessibility",
    "processing_intensity",
    "fermentation_factor",
    "retention_factor",
    "iron_bioavailability_factor",
    "protein_digestibility_factor",
    "lipid_unsaturation_index",
    "oxidation_protection_factor",
    "sodium_mg",
    "contaminant_flag_score",
    "allergen_flag_score",
    "sustainability_context_score",
    "data_quality_score",
}


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp a value to a closed interval."""
    return max(low, min(high, value))


def parse_value(key: str, value: str):
    """Parse numeric CSV values."""
    if key in NUMERIC_FIELDS:
        return float(value)
    return value


def load_rows(path: Path = DATA_FILE) -> list[dict]:
    """Load synthetic food chemistry records."""
    with path.open("r", newline="", encoding="utf-8") as handle:
        return [
            {key: parse_value(key, value) for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def energy_density_kcal_per_g(row: dict) -> float:
    """Estimate energy density."""
    total_mass = (
        row["water_g"]
        + row["protein_g"]
        + row["total_carbohydrate_g"]
        + row["total_fat_g"]
    )
    if total_mass <= 0:
        return 0.0
    return row["energy_kcal"] / total_mass


def nutrient_density_score(row: dict) -> float:
    """
    Nutrient-density proxy normalized by energy.

    This is a teaching score, not a dietary guidance system.
    """
    beneficial = (
        0.22 * clamp(row["protein_g"] / 25.0)
        + 0.20 * clamp(row["fiber_g"] / 12.0)
        + 0.14 * clamp(row["potassium_mg"] / 800.0)
        + 0.12 * clamp(row["calcium_mg"] / 400.0)
        + 0.10 * clamp(row["iron_mg"] / 6.0)
        + 0.10 * clamp(row["zinc_mg"] / 4.0)
        + 0.07 * clamp(row["vitamin_c_mg"] / 75.0)
        + 0.05 * clamp(row["folate_ug"] / 300.0)
    )

    energy_factor = max(row["energy_kcal"] / 100.0, 0.5)
    return beneficial / energy_factor


def bioavailable_iron_mg(row: dict) -> float:
    """Estimate bioavailable iron using retention and bioavailability factors."""
    return row["iron_mg"] * row["retention_factor"] * row["iron_bioavailability_factor"]


def retained_vitamin_c_mg(row: dict) -> float:
    """Estimate retained vitamin C after processing/storage."""
    return row["vitamin_c_mg"] * row["retention_factor"]


def digestible_protein_g(row: dict) -> float:
    """Estimate digestible protein."""
    return row["protein_g"] * row["protein_digestibility_factor"]


def protein_quality_proxy(row: dict) -> float:
    """Protein-quality proxy from protein amount and digestibility."""
    return clamp((digestible_protein_g(row) / 25.0) * row["protein_digestibility_factor"])


def food_matrix_protection_index(row: dict) -> float:
    """
    Estimate matrix protection.

    Less particle accessibility, more fiber, fermentation, and lower processing
    can increase matrix protection in this teaching model.
    """
    fiber_component = clamp(row["fiber_g"] / 12.0)
    intactness_component = 1.0 - row["particle_accessibility"]
    fermentation_component = 0.25 * row["fermentation_factor"]
    processing_component = 1.0 - row["processing_intensity"]

    return clamp(
        0.35 * fiber_component
        + 0.30 * intactness_component
        + 0.20 * processing_component
        + 0.15 * fermentation_component
    )


def glycemic_accessibility_proxy(row: dict) -> float:
    """
    Simplified glycemic accessibility proxy.

    Higher digestible starch, sugars, particle accessibility, and processing
    increase the proxy. Fiber and matrix protection lower it.
    """
    starch_component = clamp(row["digestible_starch_g"] / 30.0)
    sugar_component = clamp(row["total_sugars_g"] / 20.0)
    accessibility_component = row["particle_accessibility"]
    processing_component = row["processing_intensity"]
    fiber_protection = clamp(row["fiber_g"] / 12.0)
    matrix_protection = food_matrix_protection_index(row)

    return clamp(
        0.28 * starch_component
        + 0.22 * sugar_component
        + 0.20 * accessibility_component
        + 0.15 * processing_component
        - 0.10 * fiber_protection
        - 0.15 * matrix_protection
    )


def lipid_oxidation_vulnerability(row: dict) -> float:
    """
    Lipid oxidation vulnerability proxy.

    Higher unsaturation and processing increase vulnerability. Antioxidant
    protection, polyphenols, and lower water activity can reduce it.
    """
    if row["total_fat_g"] <= 0:
        return 0.0

    unsaturation = clamp(row["lipid_unsaturation_index"] / 4.5)
    processing = row["processing_intensity"]
    antioxidant = row["oxidation_protection_factor"]
    polyphenol_protection = clamp(row["polyphenol_mg"] / 300.0)
    water_activity_factor = clamp(row["water_activity"])

    return clamp(
        0.35 * unsaturation
        + 0.20 * processing
        + 0.15 * water_activity_factor
        - 0.20 * antioxidant
        - 0.10 * polyphenol_protection
    )


def sodium_pressure_index(row: dict) -> float:
    """Simplified sodium pressure proxy."""
    return clamp(row["sodium_mg"] / 600.0)


def chemical_safety_attention_index(row: dict) -> float:
    """
    Simplified food-safety attention index.

    Includes contaminant flags, allergen flags, sodium pressure, water activity,
    and data quality. This is not a safety determination.
    """
    microbial_support = clamp((row["water_activity"] - 0.85) / 0.15) if row["pH"] > 4.6 else 0.25 * clamp((row["water_activity"] - 0.85) / 0.15)
    qc_penalty = 1.0 - row["data_quality_score"]

    return clamp(
        0.28 * row["contaminant_flag_score"]
        + 0.25 * row["allergen_flag_score"]
        + 0.18 * sodium_pressure_index(row)
        + 0.17 * microbial_support
        + 0.12 * qc_penalty
    )


def nutrition_chemistry_quality_index(row: dict) -> float:
    """
    Composite food chemistry and nutrition quality proxy.

    This is not dietary guidance. It is a transparent synthetic indicator.
    """
    nutrient_density = nutrient_density_score(row)
    protein_quality = protein_quality_proxy(row)
    matrix_protection = food_matrix_protection_index(row)
    glycemic_pressure = glycemic_accessibility_proxy(row)
    oxidation_pressure = lipid_oxidation_vulnerability(row)
    safety_attention = chemical_safety_attention_index(row)

    return clamp(
        0.30 * clamp(nutrient_density)
        + 0.18 * protein_quality
        + 0.16 * matrix_protection
        + 0.12 * row["sustainability_context_score"]
        + 0.10 * row["data_quality_score"]
        - 0.08 * glycemic_pressure
        - 0.08 * oxidation_pressure
        - 0.08 * safety_attention
    )


def enrich_row(row: dict) -> dict:
    """Add advanced food chemistry indicators."""
    quality = nutrition_chemistry_quality_index(row)
    safety = chemical_safety_attention_index(row)

    if safety >= 0.65:
        flag = "review_safety_context"
    elif quality >= 0.65:
        flag = "strong_food_chemistry_profile"
    elif quality >= 0.45:
        flag = "moderate_food_chemistry_profile"
    else:
        flag = "limited_profile_or_context_needed"

    return {
        **row,
        "energy_density_kcal_per_g": energy_density_kcal_per_g(row),
        "nutrient_density_score": nutrient_density_score(row),
        "bioavailable_iron_mg": bioavailable_iron_mg(row),
        "retained_vitamin_c_mg": retained_vitamin_c_mg(row),
        "digestible_protein_g": digestible_protein_g(row),
        "protein_quality_proxy": protein_quality_proxy(row),
        "food_matrix_protection_index": food_matrix_protection_index(row),
        "glycemic_accessibility_proxy": glycemic_accessibility_proxy(row),
        "lipid_oxidation_vulnerability": lipid_oxidation_vulnerability(row),
        "sodium_pressure_index": sodium_pressure_index(row),
        "chemical_safety_attention_index": safety,
        "nutrition_chemistry_quality_index": quality,
        "profile_flag": flag,
    }


def summarize_by_food_group(rows: list[dict]) -> list[dict]:
    """Summarize indicators by food group."""
    grouped: dict[str, list[dict]] = {}

    for row in rows:
        grouped.setdefault(row["food_group"], []).append(row)

    summary = []

    for group, records in sorted(grouped.items()):
        summary.append(
            {
                "food_group": group,
                "n": len(records),
                "mean_nutrient_density_score": mean(row["nutrient_density_score"] for row in records),
                "mean_bioavailable_iron_mg": mean(row["bioavailable_iron_mg"] for row in records),
                "mean_digestible_protein_g": mean(row["digestible_protein_g"] for row in records),
                "mean_food_matrix_protection_index": mean(row["food_matrix_protection_index"] for row in records),
                "mean_glycemic_accessibility_proxy": mean(row["glycemic_accessibility_proxy"] for row in records),
                "mean_lipid_oxidation_vulnerability": mean(row["lipid_oxidation_vulnerability"] for row in records),
                "mean_chemical_safety_attention_index": mean(row["chemical_safety_attention_index"] for row in records),
                "mean_nutrition_chemistry_quality_index": mean(row["nutrition_chemistry_quality_index"] for row in records),
            }
        )

    return summary


def build_processing_retention_scenarios(base_row: dict) -> list[dict]:
    """Build nutrient-retention scenarios across processing intensity."""
    output = []

    for processing_intensity in [0.0, 0.15, 0.30, 0.50, 0.75, 0.90]:
        for retention_factor in [0.50, 0.65, 0.80, 0.95]:
            modeled = dict(base_row)
            modeled["processing_intensity"] = processing_intensity
            modeled["retention_factor"] = retention_factor

            output.append(
                {
                    "scenario": "processing_retention",
                    "food_name": base_row["food_name"],
                    "processing_intensity": processing_intensity,
                    "retention_factor": retention_factor,
                    "retained_vitamin_c_mg": retained_vitamin_c_mg(modeled),
                    "bioavailable_iron_mg": bioavailable_iron_mg(modeled),
                    "nutrition_chemistry_quality_index": nutrition_chemistry_quality_index(modeled),
                }
            )

    return output


def build_lipid_oxidation_scenarios(base_row: dict) -> list[dict]:
    """Build first-order lipid oxidation vulnerability scenario."""
    output = []

    base_vulnerability = lipid_oxidation_vulnerability(base_row)
    oxidation_rate = 0.015 + 0.08 * base_vulnerability
    initial_quality = 1.0

    for day in range(0, 181, 15):
        quality_remaining = initial_quality * math.exp(-oxidation_rate * day)

        output.append(
            {
                "scenario": "lipid_oxidation",
                "food_name": base_row["food_name"],
                "day": day,
                "oxidation_rate_proxy": oxidation_rate,
                "quality_remaining_proxy": quality_remaining,
                "lipid_oxidation_vulnerability": base_vulnerability,
            }
        )

    return output


def build_glycemic_matrix_scenarios(base_row: dict) -> list[dict]:
    """Build matrix accessibility scenarios for carbohydrate-rich foods."""
    output = []

    particle_values = [0.25, 0.50, 0.75, 0.95]
    fiber_values = [1, 4, 8, 12, 16]

    for particle in particle_values:
        for fiber in fiber_values:
            modeled = dict(base_row)
            modeled["particle_accessibility"] = particle
            modeled["fiber_g"] = fiber

            output.append(
                {
                    "scenario": "glycemic_matrix",
                    "food_name": base_row["food_name"],
                    "particle_accessibility": particle,
                    "fiber_g": fiber,
                    "food_matrix_protection_index": food_matrix_protection_index(modeled),
                    "glycemic_accessibility_proxy": glycemic_accessibility_proxy(modeled),
                }
            )

    return output


def build_mineral_bioavailability_scenarios(base_row: dict) -> list[dict]:
    """Build iron bioavailability scenarios."""
    output = []

    bioavailability_values = [0.05, 0.10, 0.15, 0.25, 0.35]
    retention_values = [0.60, 0.75, 0.90, 1.00]

    for bioavailability in bioavailability_values:
        for retention in retention_values:
            modeled = dict(base_row)
            modeled["iron_bioavailability_factor"] = bioavailability
            modeled["retention_factor"] = retention

            output.append(
                {
                    "scenario": "mineral_bioavailability",
                    "food_name": base_row["food_name"],
                    "iron_bioavailability_factor": bioavailability,
                    "retention_factor": retention,
                    "bioavailable_iron_mg": bioavailable_iron_mg(modeled),
                }
            )

    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    """Write rows to CSV."""
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict], summary: list[dict]) -> None:
    """Write Markdown report."""
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)

    strong = [row for row in rows if row["profile_flag"] == "strong_food_chemistry_profile"]
    review = [row for row in rows if row["profile_flag"] == "review_safety_context"]

    lines = [
        "# Advanced Food Chemistry and Nutrition Report",
        "",
        "Synthetic educational food chemistry and nutrition-science summary.",
        "",
        f"Foods: {len(rows)}",
        f"Strong food chemistry profiles: {len(strong)}",
        f"Safety-context review flags: {len(review)}",
        "",
        "## Strong profiles",
        "",
    ]

    for row in strong:
        lines.append(
            f"- {row['food_name']} ({row['food_group']}): "
            f"nutrient density={row['nutrient_density_score']:.3f}, "
            f"matrix protection={row['food_matrix_protection_index']:.3f}, "
            f"quality index={row['nutrition_chemistry_quality_index']:.3f}"
        )

    lines.extend(["", "## Food group summaries", ""])

    for row in summary:
        lines.append(
            f"- {row['food_group']}: "
            f"mean nutrient density={row['mean_nutrient_density_score']:.3f}, "
            f"mean matrix protection={row['mean_food_matrix_protection_index']:.3f}, "
            f"mean quality index={row['mean_nutrition_chemistry_quality_index']:.3f}"
        )

    lines.extend(["", "## Responsible-use note", ""])
    lines.append(
        "These outputs are synthetic and educational. They are not dietary advice, clinical nutrition guidance, food-safety determinations, allergen clearance, regulatory compliance findings, or product health claims."
    )

    (OUT_REPORTS / "advanced_food_chemistry_report.md").write_text("\n".join(lines), encoding="utf-8")


def write_manifest(rows, summary, retention, oxidation, glycemic, mineral) -> None:
    """Write provenance manifest."""
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "food-chemistry-molecular-basis-nutrition",
        "title": "Food Chemistry and the Molecular Basis of Nutrition",
        "advanced_layer": True,
        "synthetic_food_records": len(rows),
        "food_group_summary_rows": len(summary),
        "processing_retention_rows": len(retention),
        "lipid_oxidation_rows": len(oxidation),
        "glycemic_matrix_rows": len(glycemic),
        "mineral_bioavailability_rows": len(mineral),
        "outputs": [
            "advanced/outputs/tables/advanced_food_chemistry_indicators.csv",
            "advanced/outputs/tables/advanced_food_group_summary.csv",
            "advanced/outputs/tables/advanced_processing_retention_scenarios.csv",
            "advanced/outputs/tables/advanced_lipid_oxidation_scenarios.csv",
            "advanced/outputs/tables/advanced_glycemic_matrix_scenarios.csv",
            "advanced/outputs/tables/advanced_mineral_bioavailability_scenarios.csv",
            "advanced/outputs/reports/advanced_food_chemistry_report.md",
        ],
        "responsible_use": "Synthetic educational food chemistry workflow only; not for dietary, clinical, food-safety, allergen, regulatory, or product-claim decisions."
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows = [enrich_row(row) for row in load_rows()]
    summary = summarize_by_food_group(rows)

    orange = next(row for row in rows if row["food_name"] == "orange_segments")
    walnuts = next(row for row in rows if row["food_name"] == "walnuts")
    oats = next(row for row in rows if row["food_name"] == "oats_cooked")
    lentils = next(row for row in rows if row["food_name"] == "lentils_cooked")

    retention = build_processing_retention_scenarios(orange)
    oxidation = build_lipid_oxidation_scenarios(walnuts)
    glycemic = build_glycemic_matrix_scenarios(oats)
    mineral = build_mineral_bioavailability_scenarios(lentils)

    write_csv(OUT_TABLES / "advanced_food_chemistry_indicators.csv", rows)
    write_csv(OUT_TABLES / "advanced_food_group_summary.csv", summary)
    write_csv(OUT_TABLES / "advanced_processing_retention_scenarios.csv", retention)
    write_csv(OUT_TABLES / "advanced_lipid_oxidation_scenarios.csv", oxidation)
    write_csv(OUT_TABLES / "advanced_glycemic_matrix_scenarios.csv", glycemic)
    write_csv(OUT_TABLES / "advanced_mineral_bioavailability_scenarios.csv", mineral)

    write_report(rows, summary)
    write_manifest(rows, summary, retention, oxidation, glycemic, mineral)

    print("Advanced food chemistry workflow complete.")
    print(f"Food records: {len(rows)}")
    print(f"Food group summaries: {len(summary)}")
    print(f"Outputs written to: {OUT_TABLES.parent}")


if __name__ == "__main__":
    main()
