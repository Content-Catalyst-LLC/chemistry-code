"""
Calibration statistics scaffold.

Run from article directory:
    python python/calibration_statistics.py
"""

from pathlib import Path
import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "calibration_standards.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "python_calibration_statistics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    grouped = data.groupby("concentration_mM", as_index=False).agg(response_mean=("response", "mean"))
    slope, intercept = np.polyfit(grouped["concentration_mM"], grouped["response_mean"], deg=1)
    grouped["predicted_response"] = slope * grouped["concentration_mM"] + intercept
    grouped["residual"] = grouped["response_mean"] - grouped["predicted_response"]
    grouped["slope"] = slope
    grouped["intercept"] = intercept
    grouped["rmse"] = np.sqrt(np.mean(grouped["residual"] ** 2))

    grouped.to_csv(OUTPUT_PATH, index=False)
    print(grouped.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
