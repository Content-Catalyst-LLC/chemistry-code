#!/usr/bin/env python3
"""
Lightweight tests for the advanced geochemistry workflow.

Run from:
articles/geochemistry-chemical-history-earth/advanced/python

Command:
python3 test_geochemistry_advanced.py
"""

from geochemistry_advanced import (
    oxide_moles,
    cia_weight_based,
    cia_molar,
    isotope_delta,
    radiometric_age_ma,
    ree_normalized,
    light_to_heavy_ree_ratio,
    load_rows,
    enrich_row,
    build_radiogenic_decay_series,
    build_isotope_mixing_series,
    build_weathering_trajectory_series,
)


def test_oxide_moles_positive():
    assert oxide_moles(60.0843, "SiO2") > 0


def test_cia_values_positive():
    row = load_rows()[0]
    assert cia_weight_based(row) > 0
    assert cia_molar(row) > 0


def test_isotope_delta_zero_when_equal():
    assert abs(isotope_delta(1.0, 1.0)) < 1e-12


def test_radiometric_age_positive():
    assert radiometric_age_ma(1.0, 0.25) > 0


def test_ree_normalization_positive():
    row = load_rows()[1]
    normalized = ree_normalized(row)
    assert normalized["La_N"] > 0
    assert light_to_heavy_ree_ratio(normalized) > 0


def test_enrich_row_contains_advanced_fields():
    row = load_rows()[0]
    enriched = enrich_row(row)
    assert "CIA_molar_CaO_star" in enriched
    assert "radiometric_age_Ma_simplified" in enriched
    assert "geochemical_archive_index" in enriched


def test_decay_series_increases_daughter():
    series = build_radiogenic_decay_series(max_age_ma=500, step_ma=100)
    assert series[-1]["radiogenic_daughter_units"] > series[0]["radiogenic_daughter_units"]


def test_mixing_series_bounds():
    series = build_isotope_mixing_series()
    assert series[0]["fraction_endmember_A"] == 0
    assert series[-1]["fraction_endmember_A"] == 1


def test_weathering_trajectory_increases_cia():
    row = load_rows()[0]
    series = build_weathering_trajectory_series(row)
    assert series[-1]["modeled_CIA_molar_CaO_star"] > series[0]["modeled_CIA_molar_CaO_star"]


if __name__ == "__main__":
    test_oxide_moles_positive()
    test_cia_values_positive()
    test_isotope_delta_zero_when_equal()
    test_radiometric_age_positive()
    test_ree_normalization_positive()
    test_enrich_row_contains_advanced_fields()
    test_decay_series_increases_daughter()
    test_mixing_series_bounds()
    test_weathering_trajectory_increases_cia()
    print("All advanced geochemistry tests passed.")
