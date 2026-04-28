"""
Generate a report for Atoms, Elements, and the Periodic Organization of Matter.

Run from article directory:
    python python/06_generate_periodic_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from periodic_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "atoms_elements_periodic_report.md"

REQUIRED_OUTPUTS = [
    ("01_element_features.py", ARTICLE_DIR / "outputs" / "tables" / "element_features_summary.csv"),
    ("02_isotope_weighted_mass.py", ARTICLE_DIR / "outputs" / "tables" / "isotope_weighted_masses.csv"),
    ("03_periodic_trends.py", ARTICLE_DIR / "outputs" / "tables" / "periodic_trends.csv"),
    ("04_mole_and_composition.py", ARTICLE_DIR / "outputs" / "tables" / "mole_and_composition.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    features = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "element_features_summary.csv")
    isotopes = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "isotope_weighted_masses.csv").round(6)
    trends = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "periodic_trends.csv").round(6)
    mole = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "mole_examples_calculated.csv")
    composition = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "percent_composition.csv").round(4)

    report = [
        "# Atoms, Elements, and the Periodic Organization of Matter",
        "",
        "This report was generated from simplified educational atomic and periodic-table data.",
        "",
        "## Element Feature Summary",
        "",
        dataframe_to_markdown(features),
        "",
        "## Isotope-Weighted Atomic Masses",
        "",
        dataframe_to_markdown(isotopes),
        "",
        "## Simplified Periodic Trend Models",
        "",
        dataframe_to_markdown(trends),
        "",
        "## Mole Examples",
        "",
        dataframe_to_markdown(mole),
        "",
        "## Percent Composition",
        "",
        dataframe_to_markdown(composition),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemistry requires evaluated reference data, uncertainty analysis, source documentation, safety procedures, and professional review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
