"""
Create a radial-distribution-like pair-distance histogram scaffold.

Run from article directory:
    python python/03_radial_distribution_scaffold.py
"""

from pathlib import Path
import pandas as pd

from condensed_matter_core import radial_distribution_scaffold


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "particle_coordinates.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "radial_distribution_scaffold.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    coordinates = pd.read_csv(INPUT_PATH)
    rdf = radial_distribution_scaffold(coordinates)
    rdf.to_csv(OUTPUT_PATH, index=False)

    print(rdf.to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
