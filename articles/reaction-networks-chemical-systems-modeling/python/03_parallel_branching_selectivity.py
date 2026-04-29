"""
Calculate parallel pathway selectivity and branching outcomes.

Run from article directory:
    python python/03_parallel_branching_selectivity.py
"""

from pathlib import Path
import pandas as pd

from reaction_network_core import (
    load_stoichiometric_matrix,
    simulate_network_cases,
    parallel_selectivity,
    final_branching_outcomes,
)


ARTICLE_DIR = Path(__file__).resolve().parents[1]
PARALLEL_INPUT = ARTICLE_DIR / "data" / "parallel_cases.csv"
NETWORK_INPUT = ARTICLE_DIR / "data" / "network_cases.csv"
PARALLEL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "parallel_selectivity.csv"
BRANCHING_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "branching_outcomes.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "parallel_branching_selectivity.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    parallel = parallel_selectivity(pd.read_csv(PARALLEL_INPUT))
    _, _, stoich = load_stoichiometric_matrix(ARTICLE_DIR)
    trajectory = simulate_network_cases(pd.read_csv(NETWORK_INPUT), stoich)
    branching = final_branching_outcomes(trajectory)

    parallel.to_csv(PARALLEL_OUTPUT, index=False)
    branching.to_csv(BRANCHING_OUTPUT, index=False)

    combined = pd.concat(
        [
            parallel.astype(str).assign(table_type="parallel_selectivity"),
            branching.astype(str).assign(table_type="branching_outcomes"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Parallel selectivity")
    print(parallel.round(6).to_string(index=False))
    print("\nBranching outcomes")
    print(branching.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
