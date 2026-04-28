"""
Simulate reversible first-order approach to equilibrium.

Run from article directory:
    python python/03_reversible_dynamics.py
"""

from pathlib import Path
import pandas as pd

from equilibrium_core import simulate_reversible_dynamics


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "reversible_dynamics_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "reversible_dynamics.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = simulate_reversible_dynamics(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.head(20).round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
