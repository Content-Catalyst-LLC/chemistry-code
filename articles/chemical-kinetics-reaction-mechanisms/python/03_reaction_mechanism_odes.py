"""
Simulate consecutive reaction mechanisms A -> B -> C.

Run from article directory:
    python python/03_reaction_mechanism_odes.py
"""

from pathlib import Path
import pandas as pd

from kinetics_core import simulate_consecutive_mechanism


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "mechanism_parameters.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "reaction_mechanism_odes.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = simulate_consecutive_mechanism(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.head(20).round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
