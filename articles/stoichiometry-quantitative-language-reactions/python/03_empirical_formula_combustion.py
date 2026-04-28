"""
Calculate empirical formula ratios and combustion-analysis scaffolds.

Run from article directory:
    python python/03_empirical_formula_combustion.py
"""

from pathlib import Path
import pandas as pd

from stoichiometry_core import empirical_formula_ratios, combustion_analysis


ARTICLE_DIR = Path(__file__).resolve().parents[1]
COMPOSITION_INPUT = ARTICLE_DIR / "data" / "percent_composition_examples.csv"
COMBUSTION_INPUT = ARTICLE_DIR / "data" / "combustion_analysis_examples.csv"
COMPOSITION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "empirical_formula_ratios.csv"
COMBUSTION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "combustion_analysis.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "empirical_formula_combustion.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    empirical = empirical_formula_ratios(pd.read_csv(COMPOSITION_INPUT))
    combustion = combustion_analysis(pd.read_csv(COMBUSTION_INPUT))

    empirical.to_csv(COMPOSITION_OUTPUT, index=False)
    combustion.to_csv(COMBUSTION_OUTPUT, index=False)

    combined = pd.concat(
        [
            empirical.astype(str).assign(table_type="empirical_formula"),
            combustion.astype(str).assign(table_type="combustion_analysis"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Empirical formula ratios")
    print(empirical.round(6).to_string(index=False))
    print("\nCombustion analysis")
    print(combustion.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
