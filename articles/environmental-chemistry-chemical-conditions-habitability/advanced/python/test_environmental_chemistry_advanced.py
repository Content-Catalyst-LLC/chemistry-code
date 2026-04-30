#!/usr/bin/env python3
"""
Lightweight tests for the advanced environmental chemistry workflow.

Run from:
articles/environmental-chemistry-chemical-conditions-habitability/advanced/python

Command:
python3 test_environmental_chemistry_advanced.py
"""

from environmental_chemistry_advanced import (
    benchmark_ratio,
    concentration_load_kg_day,
    kd_L_kg,
    retardation_factor,
    henry_air_water_tendency,
    first_order_decay_constant_per_day,
    persistence_factor,
    nutrient_pressure_index,
    monte_carlo_exceedance_probability,
    load_rows,
    enrich_row,
    build_decay_scenario,
    build_leaching_retardation_scenario,
    build_multimedia_partition_scenario,
    build_exposure_pathway_scenario,
)


def test_benchmark_ratio():
    assert benchmark_ratio(12.0, 10.0) == 1.2


def test_mg_load_conversion():
    value = concentration_load_kg_day(10.0, "mg/L", 100.0)
    assert abs(value - 86.4) < 1e-9


def test_ug_load_conversion():
    value = concentration_load_kg_day(10.0, "ug/L", 100.0)
    assert abs(value - 0.0864) < 1e-9


def test_kd_positive():
    assert kd_L_kg(1000.0, 0.02) == 20.0


def test_retardation_above_one():
    value = retardation_factor(20.0, 1.5, 0.35)
    assert value > 1.0


def test_henry_tendency_range():
    value = henry_air_water_tendency(0.01)
    assert 0 <= value <= 1


def test_decay_constant_positive():
    assert first_order_decay_constant_per_day(10.0) > 0


def test_persistence_range():
    value = persistence_factor(100.0)
    assert 0 <= value <= 1


def test_nutrient_pressure_range():
    value = nutrient_pressure_index(8.0, 0.2)
    assert 0 <= value <= 1


def test_monte_carlo_probability_range():
    result = monte_carlo_exceedance_probability(12.0, 10.0, 0.9, draws=200, seed=1)
    assert 0 <= result["exceedance_probability"] <= 1
    assert result["mc_p95"] >= result["mc_p50"] >= result["mc_p05"]


def test_enrich_row_contains_advanced_fields():
    row = load_rows()[0]
    enriched = enrich_row(row)
    assert "Kd_L_kg" in enriched
    assert "retardation_factor_proxy" in enriched
    assert "chemical_habitability_pressure_index" in enriched


def test_decay_scenario_declines():
    row = next(row for row in load_rows() if row["analyte"] == "TCE")
    series = build_decay_scenario(row)
    assert series[-1]["modeled_concentration"] < series[0]["modeled_concentration"]


def test_leaching_scenario_has_rows():
    row = next(row for row in load_rows() if row["analyte"] == "arsenic")
    series = build_leaching_retardation_scenario(row)
    assert len(series) == 20


def test_partition_scenario_has_rows():
    row = next(row for row in load_rows() if row["analyte"] == "pyrene")
    series = build_multimedia_partition_scenario(row)
    assert len(series) == 12


def test_exposure_scenario_has_rows():
    row = next(row for row in load_rows() if row["analyte"] == "arsenic")
    series = build_exposure_pathway_scenario(row)
    assert len(series) == 16


if __name__ == "__main__":
    test_benchmark_ratio()
    test_mg_load_conversion()
    test_ug_load_conversion()
    test_kd_positive()
    test_retardation_above_one()
    test_henry_tendency_range()
    test_decay_constant_positive()
    test_persistence_range()
    test_nutrient_pressure_range()
    test_monte_carlo_probability_range()
    test_enrich_row_contains_advanced_fields()
    test_decay_scenario_declines()
    test_leaching_scenario_has_rows()
    test_partition_scenario_has_rows()
    test_exposure_scenario_has_rows()
    print("All advanced environmental chemistry tests passed.")
