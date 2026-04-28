"""
Calculate isotope-weighted masses and build feature matrix.

Run from article directory:
    python python/04_atomic_weight_and_features.py
"""

from pathlib import Path
import pandas as pd

from periodic_classification_core import isotope_weighted_masses, build_feature_matrix


ARTICLE_DIR = Path(__file__).resolve().parents[1]
ELEMENT_INPUT = ARTICLE_DIR / "data" / "elements_classification.csv"
ISOTOPE_INPUT = ARTICLE_DIR / "data" / "isotopes_sample.csv"
WEIGHT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "isotope_weighted_masses.csv"
FEATURE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "element_feature_matrix.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "atomic_weight_and_features.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    isotopes = pd.read_csv(ISOTOPE_INPUT)
    elements = pd.read_csv(ELEMENT_INPUT)

    weights = isotope_weighted_masses(isotopes)
    features = build_feature_matrix(elements)

    weights.to_csv(WEIGHT_OUTPUT, index=False)
    features.to_csv(FEATURE_OUTPUT, index=False)

    combined = pd.concat(
        [
            weights.astype(str).assign(table_type="isotope_weighted_masses"),
            features.astype(str).assign(table_type="element_feature_matrix"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Isotope-weighted masses")
    print(weights.round(6).to_string(index=False))
    print("\nFeature matrix")
    print(features.to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
