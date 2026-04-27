"""
Fit linear calibration and estimate unknown concentrations.

Run from article directory:
    python python/02_calibration_curve.py
"""

from pathlib import Path
import pandas as pd

from measurement_quantification_core import fit_linear_calibration, estimate_unknowns


ARTICLE_DIR = Path(__file__).resolve().parents[1]
CALIBRATION_PATH = ARTICLE_DIR / "data" / "calibration_curve.csv"
UNKNOWNS_PATH = ARTICLE_DIR / "data" / "unknown_samples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "calibration_estimates.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    calibration = pd.read_csv(CALIBRATION_PATH)
    unknowns = pd.read_csv(UNKNOWNS_PATH)

    slope, intercept = fit_linear_calibration(calibration)
    result = estimate_unknowns(unknowns, slope, intercept)
    result["calibration_slope"] = slope
    result["calibration_intercept"] = intercept

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
