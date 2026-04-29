"""
Calculate mean-squared displacement and diffusion estimates.

Run from article directory:
    python python/03_trajectory_analysis.py
"""

from pathlib import Path
import pandas as pd

from molecular_dynamics_core import trajectory_msd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "trajectory_positions.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "trajectory_analysis.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = trajectory_msd(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
