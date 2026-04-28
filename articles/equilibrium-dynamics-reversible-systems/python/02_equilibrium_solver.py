"""
Solve simple A <=> B equilibrium cases.

Run from article directory:
    python python/02_equilibrium_solver.py
"""

from pathlib import Path
import pandas as pd

from equilibrium_core import solve_simple_isomerization


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "simple_equilibrium_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "equilibrium_solver.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = solve_simple_isomerization(data)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
