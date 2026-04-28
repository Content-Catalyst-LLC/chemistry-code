"""
Apply a simple rotation matrix as a symmetry-operation illustration.

Run from article directory:
    python python/03_rotation_and_symmetry_operation.py
"""

from pathlib import Path
import pandas as pd

from geometry_core import apply_rotation_example


ARTICLE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "rotation_and_symmetry_operation.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = apply_rotation_example()
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
