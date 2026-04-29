"""
Calculate electron-density scaffold and Hückel-model energy levels.

Run from article directory:
    python python/02_density_huckel.py
"""

from pathlib import Path
import pandas as pd

from quantum_chemistry_core import electron_density, huckel_levels


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DENSITY_INPUT = ARTICLE_DIR / "data" / "electron_density_grid.csv"
HUCKEL_INPUT = ARTICLE_DIR / "data" / "huckel_cases.csv"

DENSITY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "electron_density.csv"
HUCKEL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "huckel_levels.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "density_huckel.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    density = electron_density(pd.read_csv(DENSITY_INPUT))
    huckel = huckel_levels(pd.read_csv(HUCKEL_INPUT))

    density.to_csv(DENSITY_OUTPUT, index=False)
    huckel.to_csv(HUCKEL_OUTPUT, index=False)

    combined = pd.concat(
        [
            density.astype(str).assign(table_type="electron_density"),
            huckel.astype(str).assign(table_type="huckel_levels"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Electron density")
    print(density.round(6).to_string(index=False))
    print("\nHückel levels")
    print(huckel.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
