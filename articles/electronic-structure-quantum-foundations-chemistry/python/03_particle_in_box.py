"""
Calculate particle-in-a-box energy levels.

Run from article directory:
    python python/03_particle_in_box.py
"""

from pathlib import Path
import pandas as pd

from electronic_structure_core import particle_in_box_table


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "particle_box_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "particle_in_box_levels.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    levels = particle_in_box_table(examples)
    levels.to_csv(OUTPUT_PATH, index=False)

    print(levels.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
