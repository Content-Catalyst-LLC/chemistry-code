#!/usr/bin/env python3
"""
Lightweight tests for the advanced soil chemistry workflow.

Run from:
articles/soil-chemistry-nutrient-cycles-land-systems/advanced/python

Command:
python3 test_soil_chemistry_advanced.py
"""

from soil_chemistry_advanced import (
    soc_stock_mg_ha,
    equivalent_soil_mass_proxy,
    base_saturation_percent,
    exchange_acidity_proxy,
    nitrate_leaching_vulnerability,
    phosphorus_export_proxy,
    nutrient_balance,
    load_rows,
    enrich_row,
    build_soil_carbon_scenario,
    build_nitrogen_balance_scenario,
    build_phosphorus_export_scenario,
)


def test_soc_stock_positive():
    assert soc_stock_mg_ha(2.0, 1.2, 30) > 0


def test_equivalent_soil_mass_positive():
    assert equivalent_soil_mass_proxy(1.2, 30) > 0


def test_base_saturation():
    assert abs(base_saturation_percent(8.4, 12.0) - 70.0) < 1e-9


def test_exchange_acidity():
    assert abs(exchange_acidity_proxy(12.0, 8.4) - 3.6) < 1e-9


def test_phosphorus_export_positive():
    assert phosphorus_export_proxy(5.0, 800.0) == 4.0


def test_nutrient_balance():
    assert nutrient_balance(100, 75) == 25


def test_vulnerability_in_range():
    row = load_rows()[1]
    value = nitrate_leaching_vulnerability(row)
    assert 0 <= value <= 1


def test_enrich_row_contains_advanced_fields():
    row = load_rows()[0]
    enriched = enrich_row(row)
    assert "soc_stock_Mg_ha" in enriched
    assert "base_saturation_percent" in enriched
    assert "soil_land_system_pressure_index" in enriched


def test_carbon_scenario_has_rows():
    rows = load_rows()
    series = build_soil_carbon_scenario(rows[0])
    assert len(series) > 40


def test_nitrogen_scenario_has_rows():
    rows = load_rows()
    series = build_nitrogen_balance_scenario(rows[1])
    assert len(series) == 12


def test_phosphorus_scenario_declines():
    rows = load_rows()
    series = build_phosphorus_export_scenario(rows[1])
    assert series[-1]["modeled_phosphorus_export_kg_ha"] < series[0]["modeled_phosphorus_export_kg_ha"]


if __name__ == "__main__":
    test_soc_stock_positive()
    test_equivalent_soil_mass_positive()
    test_base_saturation()
    test_exchange_acidity()
    test_phosphorus_export_positive()
    test_nutrient_balance()
    test_vulnerability_in_range()
    test_enrich_row_contains_advanced_fields()
    test_carbon_scenario_has_rows()
    test_nitrogen_scenario_has_rows()
    test_phosphorus_scenario_declines()
    print("All advanced soil chemistry tests passed.")
