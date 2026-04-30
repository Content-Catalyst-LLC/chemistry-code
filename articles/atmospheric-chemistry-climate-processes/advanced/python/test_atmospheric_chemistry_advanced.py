#!/usr/bin/env python3
"""
Lightweight tests for the advanced atmospheric chemistry workflow.

Run from:
articles/atmospheric-chemistry-climate-processes/advanced/python

Command:
python3 test_atmospheric_chemistry_advanced.py
"""

from atmospheric_chemistry_advanced import (
    reference_ratio,
    greenhouse_forcing_proxy,
    lifetime_persistence_factor,
    photochemical_ozone_index,
    aerosol_direct_effect_proxy,
    load_rows,
    enrich_row,
    build_greenhouse_scenario_series,
    build_methane_lifetime_decay_series,
    build_ozone_photochemical_scenario_series,
    build_aerosol_optical_scenario_series,
)


def test_reference_ratio():
    assert reference_ratio(420.0, 280.0) == 1.5


def test_co2_forcing_positive():
    value = greenhouse_forcing_proxy("CO2", 420.0, 280.0)
    assert value > 0


def test_ch4_forcing_positive():
    value = greenhouse_forcing_proxy("CH4", 1950.0, 722.0)
    assert value > 0


def test_lifetime_persistence_range():
    value = lifetime_persistence_factor(60.0)
    assert 0 <= value <= 1


def test_ozone_index_positive():
    value = photochemical_ozone_index(30.0, 80.0, 1.1)
    assert value > 0


def test_aerosol_direct_effect_negative_for_scattering():
    value = aerosol_direct_effect_proxy(0.2, 0.96)
    assert value < 0


def test_enrich_row_contains_advanced_fields():
    row = load_rows()[0]
    enriched = enrich_row(row)
    assert "reference_ratio" in enriched
    assert "greenhouse_forcing_proxy_W_m2" in enriched
    assert "atmospheric_chemistry_pressure_index" in enriched


def test_greenhouse_scenarios_have_rows():
    series = build_greenhouse_scenario_series()
    assert len(series) == 18


def test_methane_decay_declines():
    series = build_methane_lifetime_decay_series()
    assert series[-1]["modeled_CH4_ppb"] < series[0]["modeled_CH4_ppb"]


def test_ozone_scenarios_have_rows():
    series = build_ozone_photochemical_scenario_series()
    assert len(series) == 48


def test_aerosol_scenarios_have_rows():
    series = build_aerosol_optical_scenario_series()
    assert len(series) == 20


if __name__ == "__main__":
    test_reference_ratio()
    test_co2_forcing_positive()
    test_ch4_forcing_positive()
    test_lifetime_persistence_range()
    test_ozone_index_positive()
    test_aerosol_direct_effect_negative_for_scattering()
    test_enrich_row_contains_advanced_fields()
    test_greenhouse_scenarios_have_rows()
    test_methane_decay_declines()
    test_ozone_scenarios_have_rows()
    test_aerosol_scenarios_have_rows()
    print("All advanced atmospheric chemistry tests passed.")
