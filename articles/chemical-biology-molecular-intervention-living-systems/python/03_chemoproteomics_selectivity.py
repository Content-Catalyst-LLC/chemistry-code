"""
Calculate chemoproteomic competition and selectivity summaries.

Run from article directory:
    python python/03_chemoproteomics_selectivity.py
"""

from pathlib import Path
import pandas as pd

from chemical_biology_core import chemoproteomics_competition, selectivity_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
CHEMPROT_INPUT = ARTICLE_DIR / "data" / "chemoproteomics_competition.csv"
SELECTIVITY_INPUT = ARTICLE_DIR / "data" / "selectivity_cases.csv"

CHEMPROT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "chemoproteomics_competition_summary.csv"
SELECTIVITY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "selectivity_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "chemoproteomics_selectivity.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    chemoproteomics = chemoproteomics_competition(pd.read_csv(CHEMPROT_INPUT))
    selectivity = selectivity_summary(pd.read_csv(SELECTIVITY_INPUT))

    chemoproteomics.to_csv(CHEMPROT_OUTPUT, index=False)
    selectivity.to_csv(SELECTIVITY_OUTPUT, index=False)

    combined = pd.concat(
        [
            chemoproteomics.astype(str).assign(table_type="chemoproteomics_competition"),
            selectivity.astype(str).assign(table_type="selectivity_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Chemoproteomics competition")
    print(chemoproteomics.round(6).to_string(index=False))
    print("\nSelectivity summary")
    print(selectivity.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
