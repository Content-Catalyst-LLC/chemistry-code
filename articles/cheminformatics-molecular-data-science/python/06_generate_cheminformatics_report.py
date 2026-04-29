"""
Generate a report for Cheminformatics and Molecular Data Science.

Run from article directory:
    python python/06_generate_cheminformatics_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from cheminformatics_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "cheminformatics_report.md"

REQUIRED_OUTPUTS = [
    ("01_descriptors_graphs.py", ARTICLE_DIR / "outputs" / "tables" / "descriptors_graphs.csv"),
    ("02_fingerprints_similarity.py", ARTICLE_DIR / "outputs" / "tables" / "fingerprints_similarity.csv"),
    ("03_assay_standardization.py", ARTICLE_DIR / "outputs" / "tables" / "assay_standardization.csv"),
    ("04_splits_applicability_modeling.py", ARTICLE_DIR / "outputs" / "tables" / "splits_applicability_modeling.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    descriptors = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "descriptors_graphs.csv").round(6)
    similarity = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "fingerprints_similarity.csv").round(6)
    assays = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "assay_standardization.csv").round(6)
    split_summary = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "scaffold_split_summary.csv")
    model = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "property_modeling.csv").round(6)
    domain = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "applicability_domain.csv").round(6)

    report = [
        "# Cheminformatics and Molecular Data Science",
        "",
        "This report was generated from simplified educational cheminformatics data.",
        "",
        "## Molecular Descriptors and Graphs",
        "",
        dataframe_to_markdown(descriptors),
        "",
        "## Fingerprint Similarity",
        "",
        dataframe_to_markdown(similarity),
        "",
        "## Assay Standardization",
        "",
        dataframe_to_markdown(assays),
        "",
        "## Scaffold Split Summary",
        "",
        dataframe_to_markdown(split_summary),
        "",
        "## Simple Property Modeling",
        "",
        dataframe_to_markdown(model),
        "",
        "## Applicability Domain",
        "",
        dataframe_to_markdown(domain),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real cheminformatics requires validated chemical structures, careful standardization, assay curation, leakage-aware validation, applicability-domain checks, uncertainty reporting, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))
    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
