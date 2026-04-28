"""
Calculate centers of geometry, centers of mass, and molecular extents.

Run from article directory:
    python python/02_centers_and_extents.py
"""

from pathlib import Path
import pandas as pd

from geometry_core import centers_and_extents


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "molecular_coordinates.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "centers_and_extents.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    coordinates = pd.read_csv(INPUT_PATH)
    result = centers_and_extents(coordinates)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
