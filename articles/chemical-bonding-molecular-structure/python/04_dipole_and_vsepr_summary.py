"""
Estimate simple dipole vectors and summarize VSEPR metadata.

Run from article directory:
    python python/04_dipole_and_vsepr_summary.py
"""

from pathlib import Path
import pandas as pd

from bonding_core import estimate_dipole_vectors


ARTICLE_DIR = Path(__file__).resolve().parents[1]
COORD_INPUT = ARTICLE_DIR / "data" / "molecular_coordinates.csv"
VSEPR_INPUT = ARTICLE_DIR / "data" / "vsepr_examples.csv"
DIPOLE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "dipole_estimates.csv"
VSEPR_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vsepr_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "dipole_and_vsepr_summary.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    dipoles = estimate_dipole_vectors(pd.read_csv(COORD_INPUT))
    vsepr = pd.read_csv(VSEPR_INPUT)

    dipoles.to_csv(DIPOLE_OUTPUT, index=False)
    vsepr.to_csv(VSEPR_OUTPUT, index=False)

    combined = pd.concat(
        [
            dipoles.astype(str).assign(table_type="dipole_estimate"),
            vsepr.astype(str).assign(table_type="vsepr_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Dipole estimates")
    print(dipoles.round(6).to_string(index=False))
    print("\nVSEPR summary")
    print(vsepr.to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
