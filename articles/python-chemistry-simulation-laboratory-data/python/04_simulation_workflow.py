"""
Generate simple first-order simulation profiles.

Run from article directory:
    python python/04_simulation_workflow.py
"""

from pathlib import Path
import pandas as pd

from python_chemistry_core import simulate_first_order


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "simulation_parameters.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "simulation_workflow.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    result = simulate_first_order(pd.read_csv(INPUT_PATH))
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
