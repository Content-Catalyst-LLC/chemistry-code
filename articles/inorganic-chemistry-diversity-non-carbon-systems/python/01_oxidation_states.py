"""
Calculate oxidation-state accounting tables.

Run from article directory:
    python python/01_oxidation_states.py
"""

from pathlib import Path
import pandas as pd

from inorganic_core import oxidation_state_table


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "oxidation_state_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "oxidation_states.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = oxidation_state_table(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
