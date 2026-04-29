"""
Calculate descriptor and molecular graph scaffolds.

Run from article directory:
    python python/01_descriptors_graphs.py
"""

from pathlib import Path
import pandas as pd

from cheminformatics_core import merge_molecule_descriptors


ARTICLE_DIR = Path(__file__).resolve().parents[1]
MOLECULES_INPUT = ARTICLE_DIR / "data" / "molecules.csv"
DESCRIPTORS_INPUT = ARTICLE_DIR / "data" / "descriptors.csv"
GRAPHS_INPUT = ARTICLE_DIR / "data" / "graphs.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "descriptors_graphs.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = merge_molecule_descriptors(
        pd.read_csv(MOLECULES_INPUT),
        pd.read_csv(DESCRIPTORS_INPUT),
        pd.read_csv(GRAPHS_INPUT),
    )
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
