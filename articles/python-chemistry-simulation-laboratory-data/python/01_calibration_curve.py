"""
Fit a calibration curve and estimate unknown concentrations.

Run from article directory:
    python python/01_calibration_curve.py
"""

from pathlib import Path
import pandas as pd

from python_chemistry_core import fit_calibration, estimate_unknowns


ARTICLE_DIR = Path(__file__).resolve().parents[1]
STANDARDS_INPUT = ARTICLE_DIR / "data" / "calibration_standards.csv"
UNKNOWNS_INPUT = ARTICLE_DIR / "data" / "unknown_samples.csv"

CAL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "calibration_model.csv"
UNKNOWN_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "unknown_concentrations.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "calibration_curve.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    standards = pd.read_csv(STANDARDS_INPUT)
    unknowns = pd.read_csv(UNKNOWNS_INPUT)

    fit = fit_calibration(standards)
    unknown_summary = estimate_unknowns(unknowns, fit["slope"], fit["intercept"])

    calibration_table = fit["grouped"]
    calibration_table["slope"] = fit["slope"]
    calibration_table["intercept"] = fit["intercept"]
    calibration_table["rmse"] = fit["rmse"]

    calibration_table.to_csv(CAL_OUTPUT, index=False)
    unknown_summary.to_csv(UNKNOWN_OUTPUT, index=False)

    combined = pd.concat(
        [
            calibration_table.astype(str).assign(table_type="calibration_model"),
            unknown_summary.astype(str).assign(table_type="unknown_concentrations"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Calibration model")
    print(calibration_table.round(6).to_string(index=False))
    print("\nUnknown concentration estimates")
    print(unknown_summary.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
