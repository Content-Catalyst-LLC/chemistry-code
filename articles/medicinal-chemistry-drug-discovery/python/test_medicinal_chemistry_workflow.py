#!/usr/bin/env python3
from medicinal_chemistry_workflow import (
    pic50_from_nm,
    selectivity_window,
    lipophilic_ligand_efficiency,
    load_rows,
    enrich,
    pareto_frontier,
)

def test_pic50():
    assert abs(pic50_from_nm(10) - 8.0) < 1e-9

def test_selectivity():
    assert selectivity_window(1000, 10) == 100

def test_lle():
    assert abs(lipophilic_ligand_efficiency(10, 3) - 5) < 1e-9

def test_enrich():
    row = enrich(load_rows()[0])
    assert "multiparameter_optimization_score" in row

def test_frontier():
    rows = [enrich(row) for row in load_rows()]
    assert len(pareto_frontier(rows)) >= 1

if __name__ == "__main__":
    test_pic50()
    test_selectivity()
    test_lle()
    test_enrich()
    test_frontier()
    print("All medicinal chemistry workflow tests passed.")
