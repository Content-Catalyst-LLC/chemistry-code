"""
Generate monoprotic and polyprotic acid speciation scaffolds.

Run from article directory:
    python python/04_speciation_polyprotic.py
"""

from pathlib import Path
import pandas as pd

from acid_base_core import monoprotic_speciation, polyprotic_distribution


ARTICLE_DIR = Path(__file__).resolve().parents[1]
SPEC_INPUT = ARTICLE_DIR / "data" / "speciation_cases.csv"
POLY_INPUT = ARTICLE_DIR / "data" / "polyprotic_cases.csv"
SPEC_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "monoprotic_speciation.csv"
POLY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "polyprotic_distribution.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "speciation_polyprotic.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    mono = monoprotic_speciation(pd.read_csv(SPEC_INPUT))
    poly = polyprotic_distribution(pd.read_csv(POLY_INPUT))

    mono.to_csv(SPEC_OUTPUT, index=False)
    poly.to_csv(POLY_OUTPUT, index=False)

    combined = pd.concat(
        [
            mono.astype(str).assign(table_type="monoprotic_speciation"),
            poly.astype(str).assign(table_type="polyprotic_distribution"),
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Monoprotic speciation")
    print(mono.head(15).round(6).to_string(index=False))
    print("\nPolyprotic distribution")
    print(poly.head(15).round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
