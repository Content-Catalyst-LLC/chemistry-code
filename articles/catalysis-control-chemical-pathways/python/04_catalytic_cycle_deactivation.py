"""
Simulate catalytic-cycle and catalyst-deactivation scaffolds.

Run from article directory:
    python python/04_catalytic_cycle_deactivation.py
"""

from pathlib import Path
import pandas as pd

from catalysis_core import catalytic_cycle_simulation, deactivation_profiles


ARTICLE_DIR = Path(__file__).resolve().parents[1]
CYCLE_INPUT = ARTICLE_DIR / "data" / "catalytic_cycle_cases.csv"
DEACT_INPUT = ARTICLE_DIR / "data" / "deactivation_cases.csv"
CYCLE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "catalytic_cycle_simulation.csv"
DEACT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "deactivation_profiles.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "catalytic_cycle_deactivation.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    cycle = catalytic_cycle_simulation(pd.read_csv(CYCLE_INPUT))
    deactivation = deactivation_profiles(pd.read_csv(DEACT_INPUT))

    cycle.to_csv(CYCLE_OUTPUT, index=False)
    deactivation.to_csv(DEACT_OUTPUT, index=False)

    combined = pd.concat(
        [
            cycle.astype(str).assign(table_type="catalytic_cycle"),
            deactivation.astype(str).assign(table_type="deactivation_profile"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Catalytic cycle")
    print(cycle.head(20).round(6).to_string(index=False))
    print("\nDeactivation")
    print(deactivation.head(20).round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
