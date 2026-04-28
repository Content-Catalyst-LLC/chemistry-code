"""
Calculate formal charge and simple molecular-orbital bond order.

Run from article directory:
    python python/03_formal_charge_and_bond_order.py
"""

from pathlib import Path
import pandas as pd

from bonding_core import calculate_formal_charge, calculate_mo_bond_order


ARTICLE_DIR = Path(__file__).resolve().parents[1]
FORMAL_INPUT = ARTICLE_DIR / "data" / "formal_charge_examples.csv"
MO_INPUT = ARTICLE_DIR / "data" / "mo_bond_order_examples.csv"
FORMAL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "formal_charge.csv"
MO_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "mo_bond_order.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "formal_charge_and_bond_order.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    formal = calculate_formal_charge(pd.read_csv(FORMAL_INPUT))
    bond_order = calculate_mo_bond_order(pd.read_csv(MO_INPUT))

    formal.to_csv(FORMAL_OUTPUT, index=False)
    bond_order.to_csv(MO_OUTPUT, index=False)

    combined = pd.concat(
        [
            formal.astype(str).assign(table_type="formal_charge"),
            bond_order.astype(str).assign(table_type="mo_bond_order"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Formal charge")
    print(formal.to_string(index=False))
    print("\nMO bond order")
    print(bond_order.to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
