"""
Generate a report for Chemical Kinetics and Reaction Mechanisms.

Run from article directory:
    python python/06_generate_kinetics_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from kinetics_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "chemical_kinetics_report.md"

REQUIRED_OUTPUTS = [
    ("01_integrated_rate_laws.py", ARTICLE_DIR / "outputs" / "tables" / "integrated_rate_laws.csv"),
    ("02_arrhenius_analysis.py", ARTICLE_DIR / "outputs" / "tables" / "arrhenius_analysis.csv"),
    ("03_reaction_mechanism_odes.py", ARTICLE_DIR / "outputs" / "tables" / "reaction_mechanism_odes.csv"),
    ("04_enzyme_kinetics.py", ARTICLE_DIR / "outputs" / "tables" / "enzyme_kinetics.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    first_order = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "first_order_fit.csv").round(6)
    arrhenius = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "arrhenius_analysis.csv").round(6)
    mechanism = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "reaction_mechanism_odes.csv").round(6)
    enzyme = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "enzyme_kinetics.csv").round(6)

    report = [
        "# Chemical Kinetics and Reaction Mechanisms",
        "",
        "This report was generated from simplified educational kinetics data.",
        "",
        "## First-Order Kinetic Fits",
        "",
        dataframe_to_markdown(first_order),
        "",
        "## Arrhenius Analysis",
        "",
        dataframe_to_markdown(arrhenius),
        "",
        "## Consecutive Reaction Mechanism Trajectory",
        "",
        dataframe_to_markdown(mechanism.head(20)),
        "",
        "## Enzyme Kinetics",
        "",
        dataframe_to_markdown(enzyme),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real kinetic work requires validated measurements, clear units, temperature control, mechanistic justification, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
