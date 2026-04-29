"""
Simulate reaction-network ODE trajectories.

Run from article directory:
    python python/02_network_ode_simulation.py
"""

from pathlib import Path
import pandas as pd

from reaction_network_core import load_stoichiometric_matrix, simulate_network_cases


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "network_cases.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "network_ode_simulation.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    _, _, stoich = load_stoichiometric_matrix(ARTICLE_DIR)
    cases = pd.read_csv(INPUT_PATH)
    result = simulate_network_cases(cases, stoich)
    result.to_csv(OUTPUT_PATH, index=False)

    print(result.head(20).round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
