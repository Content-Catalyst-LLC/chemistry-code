"""
Calculate reaction enthalpy from standard formation enthalpy examples.

Run from article directory:
    python python/02_hess_law_formation_enthalpy.py
"""

from pathlib import Path
import pandas as pd

from thermodynamics_core import hess_law_reaction_enthalpy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "formation_enthalpy_examples.csv"
DETAIL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "hess_law_contributions.csv"
SUMMARY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "hess_law_formation_enthalpy.csv"


def main() -> None:
    SUMMARY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    detail, summary = hess_law_reaction_enthalpy(data)

    detail.to_csv(DETAIL_OUTPUT, index=False)
    summary.to_csv(SUMMARY_OUTPUT, index=False)

    print("Hess law summary")
    print(summary.round(6).to_string(index=False))
    print(f"Saved: {SUMMARY_OUTPUT}")


if __name__ == "__main__":
    main()
