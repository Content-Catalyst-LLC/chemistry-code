"""
Build stoichiometric matrix and reaction metadata tables.

Run from article directory:
    python python/01_stoichiometric_matrix.py
"""

from pathlib import Path
import pandas as pd

from reaction_network_core import build_stoichiometric_table


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "stoichiometric_matrix.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    stoich = build_stoichiometric_table(ARTICLE_DIR)
    species = pd.read_csv(ARTICLE_DIR / "data" / "species.csv")
    reactions = pd.read_csv(ARTICLE_DIR / "data" / "reactions.csv")

    stoich.to_csv(OUTPUT_PATH, index=False)
    species.to_csv(ARTICLE_DIR / "outputs" / "tables" / "species_metadata.csv", index=False)
    reactions.to_csv(ARTICLE_DIR / "outputs" / "tables" / "reaction_metadata.csv", index=False)

    print(stoich.to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
