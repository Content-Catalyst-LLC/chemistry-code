"""
Kinetics statistics scaffold.

Run from article directory:
    python python/kinetics_statistics.py
"""

from pathlib import Path
import math
import numpy as np
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "kinetics_timeseries.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "python_kinetics_statistics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    data["ln_concentration"] = np.log(data["concentration_mM"])

    slope, intercept = np.polyfit(data["time_s"], data["ln_concentration"], deg=1)
    k = -slope
    half_life = math.log(2.0) / k

    data["predicted_ln_concentration"] = slope * data["time_s"] + intercept
    data["predicted_concentration_mM"] = np.exp(data["predicted_ln_concentration"])
    data["residual_mM"] = data["concentration_mM"] - data["predicted_concentration_mM"]
    data["k_s_inv"] = k
    data["half_life_s"] = half_life

    data.to_csv(OUTPUT_PATH, index=False)
    print(data.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
