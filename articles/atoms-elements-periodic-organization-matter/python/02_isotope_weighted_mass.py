"""
Calculate isotope-weighted atomic masses.

Run from article directory:
    python python/02_isotope_weighted_mass.py
"""

from pathlib import Path
import pandas as pd

from periodic_core import add_atomic_identity_fields, calculate_isotope_weighted_masses


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "isotopes_sample.csv"
ENRICHED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "isotope_identity_table.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "isotope_weighted_masses.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    isotopes = pd.read_csv(INPUT_PATH)
    enriched = add_atomic_identity_fields(isotopes)
    weighted = calculate_isotope_weighted_masses(isotopes)

    enriched.to_csv(ENRICHED_OUTPUT, index=False)
    weighted.to_csv(OUTPUT_PATH, index=False)

    print("Isotope identity table")
    print(enriched.to_string(index=False))
    print("\nWeighted atomic masses")
    print(weighted.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
