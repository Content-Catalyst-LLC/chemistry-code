"""
Calculate scaffold split summaries, applicability-domain distances, and simple property-modeling outputs.

Run from article directory:
    python python/04_splits_applicability_modeling.py
"""

from pathlib import Path
import pandas as pd

from cheminformatics_core import scaffold_split_summary, simple_property_model, applicability_domain


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DESCRIPTORS_INPUT = ARTICLE_DIR / "data" / "descriptors.csv"
PROPERTIES_INPUT = ARTICLE_DIR / "data" / "property_values.csv"
SPLITS_INPUT = ARTICLE_DIR / "data" / "scaffold_splits.csv"
QUERY_INPUT = ARTICLE_DIR / "data" / "query_descriptors.csv"

SPLIT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "scaffold_split_summary.csv"
MODEL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "property_modeling.csv"
DOMAIN_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "applicability_domain.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "splits_applicability_modeling.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    descriptors = pd.read_csv(DESCRIPTORS_INPUT)
    properties = pd.read_csv(PROPERTIES_INPUT)
    splits = pd.read_csv(SPLITS_INPUT)
    queries = pd.read_csv(QUERY_INPUT)

    split_summary = scaffold_split_summary(splits)
    model = simple_property_model(descriptors, properties)
    domain = applicability_domain(descriptors, splits, queries)

    split_summary.to_csv(SPLIT_OUTPUT, index=False)
    model.to_csv(MODEL_OUTPUT, index=False)
    domain.to_csv(DOMAIN_OUTPUT, index=False)

    combined = pd.concat(
        [
            split_summary.astype(str).assign(table_type="scaffold_split_summary"),
            model.astype(str).assign(table_type="property_modeling"),
            domain.astype(str).assign(table_type="applicability_domain"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Scaffold split summary")
    print(split_summary.to_string(index=False))
    print("\nProperty modeling")
    print(model.round(6).to_string(index=False))
    print("\nApplicability domain")
    print(domain.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
