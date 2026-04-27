"""
Calculate amount of substance and molarity.

Run from article directory:
    python python/01_mass_volume_concentration.py
"""

from pathlib import Path
import pandas as pd

from measurement_quantification_core import calculate_mass_volume_concentration


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "mass_volume_concentration.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "mass_volume_concentration.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    result = calculate_mass_volume_concentration(examples)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
