"""
Calculate stoichiometry and pH examples.

Run from article directory:
    python python/01_stoichiometry_and_ph.py
"""

from pathlib import Path
import pandas as pd

from math_chemistry_core import calculate_stoichiometry, calculate_ph


ARTICLE_DIR = Path(__file__).resolve().parents[1]
STOICH_PATH = ARTICLE_DIR / "data" / "stoichiometry_examples.csv"
PH_PATH = ARTICLE_DIR / "data" / "ph_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "stoichiometry_and_ph.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    stoich = calculate_stoichiometry(pd.read_csv(STOICH_PATH))
    ph = calculate_ph(pd.read_csv(PH_PATH))

    stoich["table_type"] = "stoichiometry"
    ph["table_type"] = "ph"

    combined = pd.concat(
        [
            stoich.astype(str),
            ph.astype(str),
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(OUTPUT_PATH, index=False)

    print("Stoichiometry")
    print(stoich.round(6).to_string(index=False))
    print("\npH")
    print(ph.round(4).to_string(index=False))
    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
