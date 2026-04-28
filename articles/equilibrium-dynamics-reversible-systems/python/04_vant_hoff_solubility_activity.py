"""
Run van 't Hoff, solubility product, and activity scaffold examples.

Run from article directory:
    python python/04_vant_hoff_solubility_activity.py
"""

from pathlib import Path
import pandas as pd

from equilibrium_core import vant_hoff_fit, solubility_product_analysis, activity_scaffold


ARTICLE_DIR = Path(__file__).resolve().parents[1]

VANT_INPUT = ARTICLE_DIR / "data" / "vant_hoff_equilibrium.csv"
SOLUBILITY_INPUT = ARTICLE_DIR / "data" / "solubility_cases.csv"
ACTIVITY_INPUT = ARTICLE_DIR / "data" / "activity_cases.csv"

VANT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_fit.csv"
SOLUBILITY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "solubility_product.csv"
ACTIVITY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "activity_scaffold.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_solubility_activity.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    vant = vant_hoff_fit(pd.read_csv(VANT_INPUT))
    solubility = solubility_product_analysis(pd.read_csv(SOLUBILITY_INPUT))
    activity = activity_scaffold(pd.read_csv(ACTIVITY_INPUT))

    vant.to_csv(VANT_OUTPUT, index=False)
    solubility.to_csv(SOLUBILITY_OUTPUT, index=False)
    activity.to_csv(ACTIVITY_OUTPUT, index=False)

    combined = pd.concat(
        [
            vant.astype(str).assign(table_type="vant_hoff_fit"),
            solubility.astype(str).assign(table_type="solubility_product"),
            activity.astype(str).assign(table_type="activity_scaffold"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("van 't Hoff fit")
    print(vant.round(6).to_string(index=False))
    print("\nSolubility product")
    print(solubility.round(8).to_string(index=False))
    print("\nActivity scaffold")
    print(activity.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
