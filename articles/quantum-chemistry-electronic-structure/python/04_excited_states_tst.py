"""
Calculate electronic-state populations and transition-state-theory rates.

Run from article directory:
    python python/04_excited_states_tst.py
"""

from pathlib import Path
import pandas as pd

from quantum_chemistry_core import excited_state_populations, transition_state_theory


ARTICLE_DIR = Path(__file__).resolve().parents[1]
EXCITED_INPUT = ARTICLE_DIR / "data" / "excited_states.csv"
TST_INPUT = ARTICLE_DIR / "data" / "tst_cases.csv"

EXCITED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "excited_state_populations.csv"
TST_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "transition_state_theory.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "excited_states_tst.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    excited = excited_state_populations(pd.read_csv(EXCITED_INPUT))
    tst = transition_state_theory(pd.read_csv(TST_INPUT))

    excited.to_csv(EXCITED_OUTPUT, index=False)
    tst.to_csv(TST_OUTPUT, index=False)

    combined = pd.concat(
        [
            excited.astype(str).assign(table_type="excited_state_populations"),
            tst.astype(str).assign(table_type="transition_state_theory"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Excited-state populations")
    print(excited.round(10).to_string(index=False))
    print("\nTransition-state theory")
    print(tst.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
