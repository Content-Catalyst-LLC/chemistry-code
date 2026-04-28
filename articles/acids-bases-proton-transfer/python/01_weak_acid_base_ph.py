"""
Calculate weak acid and weak base pH scaffolds.

Run from article directory:
    python python/01_weak_acid_base_ph.py
"""

from pathlib import Path
import pandas as pd

from acid_base_core import weak_acid_ph, weak_base_ph


ARTICLE_DIR = Path(__file__).resolve().parents[1]
ACID_INPUT = ARTICLE_DIR / "data" / "weak_acid_cases.csv"
BASE_INPUT = ARTICLE_DIR / "data" / "weak_base_cases.csv"
ACID_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "weak_acid_ph.csv"
BASE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "weak_base_ph.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "weak_acid_base_ph.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    acid_results = weak_acid_ph(pd.read_csv(ACID_INPUT))
    base_results = weak_base_ph(pd.read_csv(BASE_INPUT))

    acid_results.to_csv(ACID_OUTPUT, index=False)
    base_results.to_csv(BASE_OUTPUT, index=False)

    combined = pd.concat([acid_results, base_results], ignore_index=True)
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print(combined.round(6).to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
