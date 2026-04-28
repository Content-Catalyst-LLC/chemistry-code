"""
Generate a report for Oxidation, Reduction, and Electron Transfer.

Run from article directory:
    python python/06_generate_redox_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from redox_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "redox_report.md"

REQUIRED_OUTPUTS = [
    ("01_cell_potential_gibbs.py", ARTICLE_DIR / "outputs" / "tables" / "cell_potential_gibbs.csv"),
    ("02_nernst_equation.py", ARTICLE_DIR / "outputs" / "tables" / "nernst_equation.csv"),
    ("03_redox_titration.py", ARTICLE_DIR / "outputs" / "tables" / "redox_titration.csv"),
    ("04_ph_corrosion_redox.py", ARTICLE_DIR / "outputs" / "tables" / "ph_corrosion_redox.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    cell = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "cell_potential_gibbs.csv").round(6)
    nernst = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "nernst_equation.csv").round(6)
    titration = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "redox_titration.csv").round(6)
    ph = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "ph_dependent_redox.csv").round(6)
    corrosion = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "corrosion_pairs.csv").round(6)

    report = [
        "# Oxidation, Reduction, and Electron Transfer",
        "",
        "This report was generated from simplified educational redox chemistry data.",
        "",
        "## Cell Potential and Gibbs Free Energy",
        "",
        dataframe_to_markdown(cell),
        "",
        "## Nernst Equation",
        "",
        dataframe_to_markdown(nernst),
        "",
        "## Redox Titration Electron Equivalence",
        "",
        dataframe_to_markdown(titration),
        "",
        "## pH-Dependent Redox Potential Scaffold",
        "",
        dataframe_to_markdown(ph.head(20)),
        "",
        "## Corrosion Pair Scaffold",
        "",
        dataframe_to_markdown(corrosion),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real redox analysis requires validated potentials, phase specification, pH control, activity corrections, temperature control, electrode calibration, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
