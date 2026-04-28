"""
Generate a report for The Periodic Table and the Logic of Chemical Classification.

Run from article directory:
    python python/06_generate_periodic_classification_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from periodic_classification_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "periodic_classification_report.md"

REQUIRED_OUTPUTS = [
    ("01_periodic_classification.py", ARTICLE_DIR / "outputs" / "tables" / "periodic_classification_summary.csv"),
    ("02_periodic_trends.py", ARTICLE_DIR / "outputs" / "tables" / "periodic_trends.csv"),
    ("03_element_similarity.py", ARTICLE_DIR / "outputs" / "tables" / "element_similarity.csv"),
    ("04_atomic_weight_and_features.py", ARTICLE_DIR / "outputs" / "tables" / "atomic_weight_and_features.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    classification = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "periodic_classification_summary.csv")
    trends = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "periodic_trends.csv").round(6)
    similarity = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "element_similarity.csv").round(6)
    weights = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "isotope_weighted_masses.csv").round(6)
    features = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "element_feature_matrix.csv")

    report = [
        "# The Periodic Table and the Logic of Chemical Classification",
        "",
        "This report was generated from simplified educational periodic-classification data.",
        "",
        "## Classification Summary",
        "",
        dataframe_to_markdown(classification.head(30)),
        "",
        "## Periodic Trend Models",
        "",
        dataframe_to_markdown(trends),
        "",
        "## Closest Element Pairs in Feature Space",
        "",
        dataframe_to_markdown(similarity.head(15)),
        "",
        "## Isotope-Weighted Atomic Masses",
        "",
        dataframe_to_markdown(weights),
        "",
        "## Element Feature Matrix",
        "",
        dataframe_to_markdown(features.head(20)),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real periodic-table data work requires evaluated reference data, clear units, documented classification conventions, uncertainty analysis, and expert review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
