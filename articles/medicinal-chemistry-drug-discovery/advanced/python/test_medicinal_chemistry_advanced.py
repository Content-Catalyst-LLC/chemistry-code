#!/usr/bin/env python3
"""
Lightweight tests for the advanced medicinal chemistry workflow.

Run from:
articles/medicinal-chemistry-drug-discovery/advanced/python

Command:
python3 test_medicinal_chemistry_advanced.py
"""

from medicinal_chemistry_advanced import (
    pIC50_from_nM,
    selectivity_window,
    lipophilic_ligand_efficiency,
    lipinski_violations,
    veber_violations,
    solubility_score,
    permeability_score,
    hERG_risk_score,
    cyp_inhibition_risk_score,
    multiparameter_optimization_score,
    load_rows,
    enrich_row,
    pareto_frontier,
    build_potency_lipophilicity_scenario,
    build_admet_rescue_scenario,
    build_assay_progression_matrix,
)


def test_pic50_conversion():
    assert abs(pIC50_from_nM(10.0) - 8.0) < 1e-9


def test_selectivity_window():
    assert selectivity_window(1000.0, 10.0) == 100.0


def test_lle():
    value = lipophilic_ligand_efficiency(10.0, 3.0)
    assert abs(value - 5.0) < 1e-9


def test_lipinski_violations_nonnegative():
    row = load_rows()[0]
    assert lipinski_violations(row) >= 0


def test_veber_violations_nonnegative():
    row = load_rows()[0]
    assert veber_violations(row) >= 0


def test_solubility_score_range():
    assert 0 <= solubility_score(50.0) <= 1


def test_permeability_score_range():
    assert 0 <= permeability_score(12.0) <= 1


def test_herg_risk_range():
    assert 0 <= hERG_risk_score(4.0) <= 1


def test_cyp_risk_range():
    assert 0 <= cyp_inhibition_risk_score(8.0) <= 1


def test_mpo_score_range():
    row = load_rows()[0]
    assert 0 <= multiparameter_optimization_score(row) <= 1


def test_enrich_row_contains_advanced_fields():
    row = load_rows()[0]
    enriched = enrich_row(row)
    assert "pIC50" in enriched
    assert "multiparameter_optimization_score" in enriched
    assert "advancement_recommendation" in enriched


def test_pareto_frontier_has_rows():
    indicators = [enrich_row(row) for row in load_rows()]
    frontier = pareto_frontier(indicators)
    assert len(frontier) >= 1


def test_potency_scenarios_have_rows():
    row = enrich_row(load_rows()[0])
    series = build_potency_lipophilicity_scenario(row)
    assert len(series) == 25


def test_admet_scenarios_have_rows():
    row = enrich_row(load_rows()[1])
    series = build_admet_rescue_scenario(row)
    assert len(series) == 27


def test_assay_matrix_has_rows():
    matrix = build_assay_progression_matrix()
    assert len(matrix) >= 6


if __name__ == "__main__":
    test_pic50_conversion()
    test_selectivity_window()
    test_lle()
    test_lipinski_violations_nonnegative()
    test_veber_violations_nonnegative()
    test_solubility_score_range()
    test_permeability_score_range()
    test_herg_risk_range()
    test_cyp_risk_range()
    test_mpo_score_range()
    test_enrich_row_contains_advanced_fields()
    test_pareto_frontier_has_rows()
    test_potency_scenarios_have_rows()
    test_admet_scenarios_have_rows()
    test_assay_matrix_has_rows()
    print("All advanced medicinal chemistry tests passed.")
