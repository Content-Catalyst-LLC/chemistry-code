"""
Calculate formula descriptors, DBE, and hybridization summaries.

Run from article directory:
    python python/01_formula_descriptors.py
"""

from pathlib import Path
import pandas as pd

from organic_structure_core import formula_descriptors, hybridization_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
FORMULA_INPUT = ARTICLE_DIR / "data" / "molecular_formulas.csv"
HYBRID_INPUT = ARTICLE_DIR / "data" / "carbon_hybridization_cases.csv"
FORMULA_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "formula_descriptors_only.csv"
HYBRID_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "hybridization_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "formula_descriptors.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    formula = formula_descriptors(pd.read_csv(FORMULA_INPUT))
    hybrid = hybridization_summary(pd.read_csv(HYBRID_INPUT))

    formula.to_csv(FORMULA_OUTPUT, index=False)
    hybrid.to_csv(HYBRID_OUTPUT, index=False)

    combined = pd.concat(
        [
            formula.astype(str).assign(table_type="formula_descriptors"),
            hybrid.astype(str).assign(table_type="hybridization_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Formula descriptors")
    print(formula.round(6).to_string(index=False))
    print("\nHybridization summary")
    print(hybrid.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
