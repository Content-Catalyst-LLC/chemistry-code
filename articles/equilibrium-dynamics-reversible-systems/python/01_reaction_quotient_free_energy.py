"""
Calculate reaction quotients, direction of net change, and free energy.

Run from article directory:
    python python/01_reaction_quotient_free_energy.py
"""

from pathlib import Path
import pandas as pd

from equilibrium_core import reaction_quotient_free_energy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "reaction_quotient_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "reaction_quotient_free_energy.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = reaction_quotient_free_energy(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
