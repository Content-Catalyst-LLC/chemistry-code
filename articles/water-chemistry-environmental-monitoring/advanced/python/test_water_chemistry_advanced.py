#!/usr/bin/env python3
"""
Lightweight tests for the advanced water chemistry workflow.

Run from:
articles/water-chemistry-environmental-monitoring/advanced/python

Command:
python3 test_water_chemistry_advanced.py
"""

from water_chemistry_advanced import (
    benchmark_ratio,
    concentration_load_kg_day,
    oxygen_deficit_mg_L,
    oxygen_stress_index,
    nutrient_enrichment_index,
    metal_pressure_index,
    load_rows,
    enrich_row,
    build_storm_pulse_decay_series,
    build_nutrient_load_scenarios,
    build_dissolved_oxygen_sag_series,
)


def test_benchmark_ratio():
    assert benchmark_ratio(12.0, 10.0) == 1.2


def test_mg_load_conversion():
    value = concentration_load_kg_day(10.0, "mg/L", 100.0)
    assert abs(value - 86.4) < 1e-9


def test_ug_load_conversion():
    value = concentration_load_kg_day(10.0, "ug/L", 100.0)
    assert abs(value - 0.0864) < 1e-9


def test_oxygen_deficit():
    assert oxygen_deficit_mg_L(7.0, 9.0) == 2.0


def test_oxygen_stress_range():
    value = oxygen_stress_index(4.0, 9.0)
    assert 0 <= value <= 1


def test_nutrient_index_range():
    value = nutrient_enrichment_index(7.8, 0.18)
    assert 0 <= value <= 1


def test_metal_index_range():
    value = metal_pressure_index(18.0, 14.0, 12.0)
    assert 0 <= value <= 1


def test_enrich_row_contains_advanced_fields():
    row = load_rows()[0]
    enriched = enrich_row(row)
    assert "benchmark_ratio" in enriched
    assert "water_quality_pressure_index" in enriched
    assert "evidence_weighted_pressure_index" in enriched


def test_storm_pulse_declines():
    row = next(row for row in load_rows() if row["site"] == "Storm-D")
    series = build_storm_pulse_decay_series(row)
    assert series[-1]["modeled_concentration"] < series[0]["modeled_concentration"]


def test_nutrient_scenarios_have_rows():
    row = next(row for row in load_rows() if row["analyte"] == "nitrate_as_N")
    series = build_nutrient_load_scenarios(row)
    assert len(series) == 20


def test_oxygen_sag_recovers():
    row = next(row for row in load_rows() if row["site"] == "Lake-B")
    series = build_dissolved_oxygen_sag_series(row)
    assert series[-1]["modeled_dissolved_oxygen_mg_L"] > series[0]["modeled_dissolved_oxygen_mg_L"]


if __name__ == "__main__":
    test_benchmark_ratio()
    test_mg_load_conversion()
    test_ug_load_conversion()
    test_oxygen_deficit()
    test_oxygen_stress_range()
    test_nutrient_index_range()
    test_metal_index_range()
    test_enrich_row_contains_advanced_fields()
    test_storm_pulse_declines()
    test_nutrient_scenarios_have_rows()
    test_oxygen_sag_recovers()
    print("All advanced water chemistry tests passed.")
