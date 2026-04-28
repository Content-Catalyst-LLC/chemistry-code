"""
Calculate limiting reagent, theoretical yield, and percent yield.

Run from article directory:
    python python/01_limiting_reagent_yield.py
"""

from pathlib import Path
import pandas as pd

from stoichiometry_core import limiting_reagent_and_yield


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REACTIONS_INPUT = ARTICLE_DIR / "data" / "reactions.csv"
EXAMPLES_INPUT = ARTICLE_DIR / "data" / "limiting_reagent_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "limiting_reagent_yield.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    reactions = pd.read_csv(REACTIONS_INPUT)
    examples = pd.read_csv(EXAMPLES_INPUT)
    result = limiting_reagent_and_yield(reactions, examples)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
