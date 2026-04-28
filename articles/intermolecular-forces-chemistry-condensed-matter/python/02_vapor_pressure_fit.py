"""
Fit a Clausius-Clapeyron-style relationship for synthetic vapor-pressure data.

Run from article directory:
    python python/02_vapor_pressure_fit.py
"""

from pathlib import Path
import pandas as pd

from condensed_matter_core import fit_vapor_pressure


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "vapor_pressure_sample.csv"
TRANSFORMED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vapor_pressure_transformed.csv"
FIT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vapor_pressure_fit.csv"


def main() -> None:
    FIT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    vapor = pd.read_csv(INPUT_PATH)
    transformed, fit = fit_vapor_pressure(vapor)

    transformed.to_csv(TRANSFORMED_OUTPUT, index=False)
    fit.to_csv(FIT_OUTPUT, index=False)

    print("Vapor pressure fit")
    print(fit.round(6).to_string(index=False))
    print(f"Saved: {FIT_OUTPUT}")


if __name__ == "__main__":
    main()
