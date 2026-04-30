#!/usr/bin/env python3
"""
Lightweight tests for the advanced toxicology workflow.

Run from:
articles/toxicology-exposure-chemical-risk/advanced/python

Command:
python3 test_toxicology_exposure_advanced.py
"""

from toxicology_exposure_advanced import (
    load_rows,
    chronic_daily_intake,
    absorbed_dose,
    hazard_quotient,
    margin_of_exposure,
    cancer_risk_proxy,
    monte_carlo_uncertainty,
    enrich_row,
    summarize_hazard_index,
    build_exposure_reduction_scenarios,
    build_body_weight_vulnerability_scenarios,
    build_mixture_scenarios,
)


def test_cdi_positive():
    row = load_rows()[0]
    assert chronic_daily_intake(row) > 0


def test_absorbed_dose_positive():
    row = load_rows()[0]
    assert absorbed_dose(row) > 0


def test_hazard_quotient_nonnegative():
    row = load_rows()[0]
    assert hazard_quotient(row) >= 0


def test_margin_of_exposure_positive():
    row = load_rows()[0]
    assert margin_of_exposure(row) > 0


def test_cancer_risk_nonnegative():
    row = load_rows()[0]
    assert cancer_risk_proxy(row) >= 0


def test_monte_carlo_range():
    row = load_rows()[0]
    result = monte_carlo_uncertainty(row, draws=100)
    assert 0 <= result["mc_probability_hq_above_1"] <= 1
    assert result["mc_hq_p95"] >= result["mc_hq_p50"] >= result["mc_hq_p05"]


def test_enrich_row_fields():
    row = enrich_row(load_rows()[0])
    assert "hazard_quotient" in row
    assert "evidence_weighted_risk_index" in row
    assert "attention_flag" in row


def test_summary_has_rows():
    rows = [enrich_row(row) for row in load_rows()]
    summary = summarize_hazard_index(rows, "target_system")
    assert len(summary) >= 1


def test_exposure_reduction_declines():
    row = enrich_row(load_rows()[0])
    series = build_exposure_reduction_scenarios(row)
    assert series[-1]["modeled_hazard_quotient"] < series[0]["modeled_hazard_quotient"]


def test_body_weight_scenarios_have_rows():
    row = enrich_row(load_rows()[2])
    series = build_body_weight_vulnerability_scenarios(row)
    assert len(series) == 24


def test_mixture_scenarios_have_rows():
    rows = [enrich_row(row) for row in load_rows()]
    series = build_mixture_scenarios(rows)
    assert len(series) == len(rows)


if __name__ == "__main__":
    test_cdi_positive()
    test_absorbed_dose_positive()
    test_hazard_quotient_nonnegative()
    test_margin_of_exposure_positive()
    test_cancer_risk_nonnegative()
    test_monte_carlo_range()
    test_enrich_row_fields()
    test_summary_has_rows()
    test_exposure_reduction_declines()
    test_body_weight_scenarios_have_rows()
    test_mixture_scenarios_have_rows()
    print("All advanced toxicology tests passed.")
