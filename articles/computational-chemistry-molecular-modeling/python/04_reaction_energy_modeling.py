"""
Calculate reaction-energy scaffolds and toy molecular dynamics update.

Run from article directory:
    python python/04_reaction_energy_modeling.py
"""

from pathlib import Path
import pandas as pd

from computational_chemistry_core import reaction_energy_table, toy_md_step


ARTICLE_DIR = Path(__file__).resolve().parents[1]
RXN_INPUT = ARTICLE_DIR / "data" / "reaction_energies.csv"
MD_INPUT = ARTICLE_DIR / "data" / "md_toy_initial.csv"

RXN_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "reaction_energy_table.csv"
MD_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "toy_md_step.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "reaction_energy_modeling.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    rxn = reaction_energy_table(pd.read_csv(RXN_INPUT))
    md = toy_md_step(pd.read_csv(MD_INPUT))

    rxn.to_csv(RXN_OUTPUT, index=False)
    md.to_csv(MD_OUTPUT, index=False)

    combined = pd.concat(
        [
            rxn.astype(str).assign(table_type="reaction_energy_table"),
            md.astype(str).assign(table_type="toy_md_step"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Reaction energy table")
    print(rxn.round(6).to_string(index=False))
    print("\nToy MD step")
    print(md.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
