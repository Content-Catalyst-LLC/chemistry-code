"""
Fit first-order kinetic data and generate integrated rate-law trajectories.

Run from article directory:
    python python/01_integrated_rate_laws.py
"""

from pathlib import Path
import pandas as pd

from kinetics_core import fit_first_order, integrated_rate_law_trajectories


ARTICLE_DIR = Path(__file__).resolve().parents[1]
FIRST_ORDER_INPUT = ARTICLE_DIR / "data" / "first_order_data.csv"
ORDER_INPUT = ARTICLE_DIR / "data" / "reaction_order_examples.csv"
FIT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "first_order_fit.csv"
TRAJECTORY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "integrated_rate_law_trajectories.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "integrated_rate_laws.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    first_order = pd.read_csv(FIRST_ORDER_INPUT)
    order_examples = pd.read_csv(ORDER_INPUT)

    fit = fit_first_order(first_order)
    trajectories = integrated_rate_law_trajectories(order_examples)

    fit.to_csv(FIT_OUTPUT, index=False)
    trajectories.to_csv(TRAJECTORY_OUTPUT, index=False)

    combined = pd.concat(
        [
            fit.astype(str).assign(table_type="first_order_fit"),
            trajectories.astype(str).assign(table_type="integrated_trajectories"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("First-order fit")
    print(fit.round(6).to_string(index=False))
    print("\nIntegrated trajectories")
    print(trajectories.head(18).round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
