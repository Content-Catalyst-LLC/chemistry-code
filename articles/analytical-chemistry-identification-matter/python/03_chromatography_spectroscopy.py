"""
Calculate chromatographic resolution and Beer-Lambert quantification.

Run from article directory:
    python python/03_chromatography_spectroscopy.py
"""

from pathlib import Path
import pandas as pd

from analytical_core import chromatographic_resolution, beer_lambert_quantification


ARTICLE_DIR = Path(__file__).resolve().parents[1]
CHROM_INPUT = ARTICLE_DIR / "data" / "chromatography_peaks.csv"
BEER_INPUT = ARTICLE_DIR / "data" / "beer_lambert_cases.csv"

CHROM_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "chromatographic_resolution.csv"
BEER_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "beer_lambert_quantification.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "chromatography_spectroscopy.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    chrom = chromatographic_resolution(pd.read_csv(CHROM_INPUT))
    beer = beer_lambert_quantification(pd.read_csv(BEER_INPUT))

    chrom.to_csv(CHROM_OUTPUT, index=False)
    beer.to_csv(BEER_OUTPUT, index=False)

    combined = pd.concat(
        [
            chrom.astype(str).assign(table_type="chromatographic_resolution"),
            beer.astype(str).assign(table_type="beer_lambert_quantification"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Chromatographic resolution")
    print(chrom.round(6).to_string(index=False))
    print("\nBeer-Lambert quantification")
    print(beer.round(10).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
