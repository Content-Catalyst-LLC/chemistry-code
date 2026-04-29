"""
Calculate protein-ligand binding occupancy.

Run from article directory:
    python python/02_binding_occupancy.py
"""

from pathlib import Path
import pandas as pd

from biochemistry_core import binding_occupancy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "binding_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "binding_occupancy.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = binding_occupancy(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
