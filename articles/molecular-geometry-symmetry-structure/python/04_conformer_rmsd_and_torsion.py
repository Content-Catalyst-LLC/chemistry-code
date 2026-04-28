"""
Calculate conformer RMSD and summarize VSEPR metadata.

Run from article directory:
    python python/04_conformer_rmsd_and_torsion.py
"""

from pathlib import Path
import pandas as pd

from geometry_core import conformer_rmsd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
CONFORMER_INPUT = ARTICLE_DIR / "data" / "conformer_coordinates.csv"
VSEPR_INPUT = ARTICLE_DIR / "data" / "vsepr_examples.csv"

RMSD_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "conformer_rmsd.csv"
VSEPR_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vsepr_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "conformer_rmsd_and_torsion.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    conformers = pd.read_csv(CONFORMER_INPUT)
    vsepr = pd.read_csv(VSEPR_INPUT)
    rmsd = conformer_rmsd(conformers)

    rmsd.to_csv(RMSD_OUTPUT, index=False)
    vsepr.to_csv(VSEPR_OUTPUT, index=False)

    combined = pd.concat(
        [
            rmsd.astype(str).assign(table_type="conformer_rmsd"),
            vsepr.astype(str).assign(table_type="vsepr_summary"),
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Conformer RMSD")
    print(rmsd.round(6).to_string(index=False))
    print("\nVSEPR summary")
    print(vsepr.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
