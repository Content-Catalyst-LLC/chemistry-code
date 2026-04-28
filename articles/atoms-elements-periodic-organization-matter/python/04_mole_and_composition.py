"""
Calculate mole conversions and percent composition.

Run from article directory:
    python python/04_mole_and_composition.py
"""

from pathlib import Path
import pandas as pd

from periodic_core import calculate_mole_examples, calculate_percent_composition


ARTICLE_DIR = Path(__file__).resolve().parents[1]
MOLE_INPUT = ARTICLE_DIR / "data" / "mole_examples.csv"
COMPOUND_INPUT = ARTICLE_DIR / "data" / "compounds_sample.csv"
MOLE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "mole_examples_calculated.csv"
COMPOSITION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "percent_composition.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "mole_and_composition.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    mole_results = calculate_mole_examples(pd.read_csv(MOLE_INPUT))
    composition = calculate_percent_composition(pd.read_csv(COMPOUND_INPUT))

    mole_results.to_csv(MOLE_OUTPUT, index=False)
    composition.to_csv(COMPOSITION_OUTPUT, index=False)

    combined = pd.concat(
        [
            mole_results.astype(str).assign(table_type="mole_examples"),
            composition.astype(str).assign(table_type="percent_composition"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Mole examples")
    print(mole_results.to_string(index=False))
    print("\nPercent composition")
    print(composition.round(4).to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
