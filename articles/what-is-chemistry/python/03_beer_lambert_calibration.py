"""
Fit a simple Beer-Lambert calibration curve.

Run from article directory:
    python python/03_beer_lambert_calibration.py
"""

from pathlib import Path
import pandas as pd

from chemistry_intro_core import beer_lambert_fit


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "beer_lambert_calibration.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "beer_lambert_fit.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    calibration = pd.read_csv(INPUT_PATH)
    fit = beer_lambert_fit(calibration)

    result = pd.DataFrame([fit])
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
