"""
Generate a report for What Is Chemistry?

Run from article directory:
    python python/06_generate_chemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from chemistry_intro_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "what_is_chemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_moles_molarity_dilution.py", ARTICLE_DIR / "outputs" / "tables" / "moles_molarity_dilution.csv"),
    ("02_first_order_kinetics.py", ARTICLE_DIR / "outputs" / "tables" / "first_order_kinetics.csv"),
    ("03_beer_lambert_calibration.py", ARTICLE_DIR / "outputs" / "tables" / "beer_lambert_fit.csv"),
    ("04_ph_calculations.py", ARTICLE_DIR / "outputs" / "tables" / "ph_calculations.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    moles = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "moles_molarity_dilution.csv").round(5)
    kinetics = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "first_order_kinetics.csv").round(5)
    beer = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "beer_lambert_fit.csv").round(5)
    ph = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "ph_calculations.csv").round(4)

    report = [
        "# What Is Chemistry?",
        "",
        "This report was generated from synthetic educational chemistry data.",
        "",
        "## Moles and Molarity",
        "",
        dataframe_to_markdown(moles[["substance", "formula", "moles", "molarity_mol_l"]]),
        "",
        "## First-Order Kinetics",
        "",
        dataframe_to_markdown(kinetics.head(10)),
        "",
        "## Beer-Lambert Calibration",
        "",
        dataframe_to_markdown(beer),
        "",
        "## pH Calculations",
        "",
        dataframe_to_markdown(ph),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemistry requires validated methods, safety procedures, calibration, uncertainty analysis, and professional review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
