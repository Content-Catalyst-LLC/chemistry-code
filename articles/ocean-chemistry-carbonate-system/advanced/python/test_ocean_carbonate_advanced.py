#!/usr/bin/env python3
"""
Lightweight tests for the advanced ocean carbonate workflow.

Run from:
articles/ocean-chemistry-carbonate-system/advanced/python

Command:
python3 test_ocean_carbonate_advanced.py
"""

from ocean_carbonate_advanced import (
    carbonate_fractions,
    carbonate_species_umol_kg,
    saturation_state,
    air_sea_co2_flux_proxy,
    revelle_factor_intuition_proxy,
    load_rows,
    enrich_row,
    build_sensitivity_series,
)


def test_carbonate_fractions_sum_to_one():
    fractions = carbonate_fractions(8.1)
    total = fractions["alpha_CO2_star"] + fractions["alpha_HCO3"] + fractions["alpha_CO3"]
    assert abs(total - 1.0) < 1e-9


def test_species_sum_to_dic():
    species = carbonate_species_umol_kg(8.1, 2050.0)
    total = (
        species["CO2_star_umol_kg"]
        + species["bicarbonate_umol_kg"]
        + species["carbonate_umol_kg"]
    )
    assert abs(total - 2050.0) < 1e-6


def test_saturation_state_positive():
    omega = saturation_state(10.3, 150.0, 6.5e-7)
    assert omega > 0


def test_flux_proxy_sign():
    uptake = air_sea_co2_flux_proxy(410, 420, 6.0)
    outgassing = air_sea_co2_flux_proxy(820, 420, 8.5)
    assert uptake < 0
    assert outgassing > 0


def test_revelle_proxy_positive():
    proxy = revelle_factor_intuition_proxy(8.05, 2050, 2310)
    assert proxy > 0


def test_workflow_rows():
    rows = load_rows()
    indicators = [enrich_row(row) for row in rows]
    assert len(indicators) == len(rows)
    assert "omega_aragonite_simplified" in indicators[0]
    assert "acidification_pressure_index" in indicators[0]


def test_sensitivity_series_declines():
    row = load_rows()[0]
    series = build_sensitivity_series(row)
    assert len(series) > 5
    assert series[-1]["modeled_pH_total_scale"] < series[0]["modeled_pH_total_scale"]


if __name__ == "__main__":
    test_carbonate_fractions_sum_to_one()
    test_species_sum_to_dic()
    test_saturation_state_positive()
    test_flux_proxy_sign()
    test_revelle_proxy_positive()
    test_workflow_rows()
    test_sensitivity_series_declines()
    print("All advanced ocean carbonate tests passed.")
