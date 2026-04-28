"""
Generate a report for Chemical Bonding and Molecular Structure.

Run from article directory:
    python python/06_generate_bonding_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from bonding_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "chemical_bonding_report.md"

REQUIRED_OUTPUTS = [
    ("01_bond_geometry.py", ARTICLE_DIR / "outputs" / "tables" / "bond_geometry.csv"),
    ("02_bond_polarity.py", ARTICLE_DIR / "outputs" / "tables" / "bond_polarity.csv"),
    ("03_formal_charge_and_bond_order.py", ARTICLE_DIR / "outputs" / "tables" / "formal_charge_and_bond_order.csv"),
    ("04_dipole_and_vsepr_summary.py", ARTICLE_DIR / "outputs" / "tables" / "dipole_and_vsepr_summary.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    distances = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "bond_distances.csv").round(6)
    angles = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "bond_angles.csv").round(3)
    polarity = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "bond_polarity.csv").round(4)
    formal = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "formal_charge.csv")
    bond_order = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "mo_bond_order.csv")
    dipoles = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "dipole_estimates.csv").round(6)
    vsepr = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "vsepr_summary.csv")

    report = [
        "# Chemical Bonding and Molecular Structure",
        "",
        "This report was generated from simplified educational bonding and molecular-structure data.",
        "",
        "## Bond Distances",
        "",
        dataframe_to_markdown(distances),
        "",
        "## Bond Angles",
        "",
        dataframe_to_markdown(angles),
        "",
        "## Bond Polarity",
        "",
        dataframe_to_markdown(polarity),
        "",
        "## Formal Charge",
        "",
        dataframe_to_markdown(formal),
        "",
        "## Molecular-Orbital Bond Order",
        "",
        dataframe_to_markdown(bond_order),
        "",
        "## Dipole Estimates",
        "",
        dataframe_to_markdown(dipoles),
        "",
        "## VSEPR Summary",
        "",
        dataframe_to_markdown(vsepr),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemical bonding and molecular structure work requires validated data, chemically meaningful models, uncertainty analysis, experimental evidence, and expert review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
