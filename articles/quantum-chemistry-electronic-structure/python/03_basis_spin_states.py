"""
Calculate basis-set convergence and spin-state comparisons.

Run from article directory:
    python python/03_basis_spin_states.py
"""

from pathlib import Path
import pandas as pd

from quantum_chemistry_core import basis_convergence, spin_state_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
BASIS_INPUT = ARTICLE_DIR / "data" / "basis_convergence.csv"
SPIN_INPUT = ARTICLE_DIR / "data" / "spin_state_cases.csv"

BASIS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "basis_convergence.csv"
SPIN_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "spin_state_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "basis_spin_states.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    basis = basis_convergence(pd.read_csv(BASIS_INPUT))
    spin = spin_state_summary(pd.read_csv(SPIN_INPUT))

    basis.to_csv(BASIS_OUTPUT, index=False)
    spin.to_csv(SPIN_OUTPUT, index=False)

    combined = pd.concat(
        [
            basis.astype(str).assign(table_type="basis_convergence"),
            spin.astype(str).assign(table_type="spin_state_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Basis convergence")
    print(basis.round(6).to_string(index=False))
    print("\nSpin-state summary")
    print(spin.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
