#!/usr/bin/env python3
"""
Lightweight tests for the advanced food chemistry workflow.

Run from:
articles/food-chemistry-molecular-basis-nutrition/advanced/python

Command:
python3 test_food_chemistry_advanced.py
"""

from food_chemistry_advanced import (
    load_rows,
    energy_density_kcal_per_g,
    nutrient_density_score,
    bioavailable_iron_mg,
    retained_vitamin_c_mg,
    digestible_protein_g,
    glycemic_accessibility_proxy,
    lipid_oxidation_vulnerability,
    enrich_row,
    summarize_by_food_group,
    build_processing_retention_scenarios,
    build_lipid_oxidation_scenarios,
    build_glycemic_matrix_scenarios,
    build_mineral_bioavailability_scenarios,
)


def test_energy_density_positive():
    row = load_rows()[0]
    assert energy_density_kcal_per_g(row) > 0


def test_nutrient_density_nonnegative():
    row = load_rows()[0]
    assert nutrient_density_score(row) >= 0


def test_bioavailable_iron_nonnegative():
    row = load_rows()[0]
    assert bioavailable_iron_mg(row) >= 0


def test_retained_vitamin_c_nonnegative():
    row = load_rows()[4]
    assert retained_vitamin_c_mg(row) >= 0


def test_digestible_protein_nonnegative():
    row = load_rows()[0]
    assert digestible_protein_g(row) >= 0


def test_glycemic_proxy_range():
    row = load_rows()[1]
    value = glycemic_accessibility_proxy(row)
    assert 0 <= value <= 1


def test_lipid_oxidation_range():
    row = load_rows()[3]
    value = lipid_oxidation_vulnerability(row)
    assert 0 <= value <= 1


def test_enrich_row_fields():
    row = enrich_row(load_rows()[0])
    assert "nutrition_chemistry_quality_index" in row
    assert "profile_flag" in row


def test_summary_has_rows():
    rows = [enrich_row(row) for row in load_rows()]
    summary = summarize_by_food_group(rows)
    assert len(summary) >= 1


def test_retention_scenarios_have_rows():
    row = next(row for row in load_rows() if row["food_name"] == "orange_segments")
    assert len(build_processing_retention_scenarios(row)) == 24


def test_oxidation_scenarios_decline():
    row = next(row for row in load_rows() if row["food_name"] == "walnuts")
    series = build_lipid_oxidation_scenarios(row)
    assert series[-1]["quality_remaining_proxy"] < series[0]["quality_remaining_proxy"]


def test_glycemic_scenarios_have_rows():
    row = next(row for row in load_rows() if row["food_name"] == "oats_cooked")
    assert len(build_glycemic_matrix_scenarios(row)) == 20


def test_mineral_scenarios_have_rows():
    row = next(row for row in load_rows() if row["food_name"] == "lentils_cooked")
    assert len(build_mineral_bioavailability_scenarios(row)) == 20


if __name__ == "__main__":
    test_energy_density_positive()
    test_nutrient_density_nonnegative()
    test_bioavailable_iron_nonnegative()
    test_retained_vitamin_c_nonnegative()
    test_digestible_protein_nonnegative()
    test_glycemic_proxy_range()
    test_lipid_oxidation_range()
    test_enrich_row_fields()
    test_summary_has_rows()
    test_retention_scenarios_have_rows()
    test_oxidation_scenarios_decline()
    test_glycemic_scenarios_have_rows()
    test_mineral_scenarios_have_rows()
    print("All advanced food chemistry tests passed.")
