"""
Fit first-order kinetics and calculate Arrhenius transformation.

Run from article directory:
    python python/02_kinetics_analysis.py
"""

from pathlib import Path
import pandas as pd

from python_chemistry_core import first_order_kinetics, arrhenius_transform


ARTICLE_DIR = Path(__file__).resolve().parents[1]
KINETICS_INPUT = ARTICLE_DIR / "data" / "kinetics_timeseries.csv"
ARRHENIUS_INPUT = ARTICLE_DIR / "data" / "arrhenius_rates.csv"

KINETICS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "first_order_kinetics.csv"
ARRHENIUS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "arrhenius_transform.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "kinetics_analysis.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    kinetics = first_order_kinetics(pd.read_csv(KINETICS_INPUT))
    arrhenius = arrhenius_transform(pd.read_csv(ARRHENIUS_INPUT))

    kinetics.to_csv(KINETICS_OUTPUT, index=False)
    arrhenius.to_csv(ARRHENIUS_OUTPUT, index=False)

    combined = pd.concat(
        [
            kinetics.astype(str).assign(table_type="first_order_kinetics"),
            arrhenius.astype(str).assign(table_type="arrhenius_transform"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("First-order kinetics")
    print(kinetics.round(6).to_string(index=False))
    print("\nArrhenius transform")
    print(arrhenius.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
