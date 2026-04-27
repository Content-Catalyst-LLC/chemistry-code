"""
Simulate first-order kinetics.

Run from article directory:
    python python/02_first_order_kinetics.py
"""

from pathlib import Path
import pandas as pd

from chemistry_intro_core import simulate_first_order


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "kinetics_examples.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "first_order_kinetics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    examples = pd.read_csv(INPUT_PATH)
    trajectories = [simulate_first_order(row) for _, row in examples.iterrows()]
    result = pd.concat(trajectories, ignore_index=True)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(5).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
