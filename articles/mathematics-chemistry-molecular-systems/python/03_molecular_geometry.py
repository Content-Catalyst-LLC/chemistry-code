"""
Calculate molecular distances from coordinates.

Run from article directory:
    python python/03_molecular_geometry.py
"""

from pathlib import Path
import pandas as pd

from math_chemistry_core import calculate_molecular_distances


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "molecular_coordinates.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "molecular_distances.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    coordinates = pd.read_csv(INPUT_PATH)
    distances = calculate_molecular_distances(coordinates)

    distances.to_csv(OUTPUT_PATH, index=False)

    print(distances.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
