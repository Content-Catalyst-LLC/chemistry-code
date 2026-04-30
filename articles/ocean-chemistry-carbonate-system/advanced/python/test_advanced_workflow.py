
#!/usr/bin/env python3
"""
Lightweight tests for the article-specific advanced workflow.
"""

from advanced_workflow import (
    ratio_safe,
    first_order_series,
    carbonate_fractions,
    isotope_delta,
    radiometric_age_ma,
    load_rows,
    run_model,
)

def test_ratio_safe():
    assert ratio_safe(10, 2) == 5
    assert ratio_safe(10, 0) == 0.0

def test_first_order_series():
    rows = first_order_series(100, 0.1, 3, 1.0, "x")
    assert len(rows) == 4
    assert rows[-1]["x"] < rows[0]["x"]

def test_carbonate_fractions():
    f = carbonate_fractions(8.1)
    total = f["alpha_CO2_star"] + f["alpha_HCO3"] + f["alpha_CO3"]
    assert abs(total - 1.0) < 1e-9

def test_isotope_delta():
    assert abs(isotope_delta(1.01, 1.0) - 10.0) < 1e-9

def test_radiometric_age():
    assert radiometric_age_ma(1.0, 0.1) > 0

def test_model_runs():
    rows = load_rows()
    indicators, series = run_model(rows)
    assert len(indicators) == len(rows)
    assert len(series) > 0

if __name__ == "__main__":
    test_ratio_safe()
    test_first_order_series()
    test_carbonate_fractions()
    test_isotope_delta()
    test_radiometric_age()
    test_model_runs()
    print("All advanced workflow tests passed.")
