"""
Summarize coordination complexes and ligand descriptors.

Run from article directory:
    python python/02_coordination_ligands.py
"""

from pathlib import Path
import pandas as pd

from inorganic_core import coordination_summary, ligand_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
COORD_INPUT = ARTICLE_DIR / "data" / "coordination_cases.csv"
LIGAND_INPUT = ARTICLE_DIR / "data" / "ligand_cases.csv"
COORD_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "coordination_summary.csv"
LIGAND_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "ligand_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "coordination_ligands.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    coordination = coordination_summary(pd.read_csv(COORD_INPUT))
    ligands = ligand_summary(pd.read_csv(LIGAND_INPUT))

    coordination.to_csv(COORD_OUTPUT, index=False)
    ligands.to_csv(LIGAND_OUTPUT, index=False)

    combined = pd.concat(
        [
            coordination.astype(str).assign(table_type="coordination_summary"),
            ligands.astype(str).assign(table_type="ligand_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Coordination summary")
    print(coordination.to_string(index=False))
    print("\nLigand summary")
    print(ligands.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
