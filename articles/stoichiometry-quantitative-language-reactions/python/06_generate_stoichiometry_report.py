"""
Generate a report for Stoichiometry and the Quantitative Language of Reactions.

Run from article directory:
    python python/06_generate_stoichiometry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from stoichiometry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "stoichiometry_report.md"

REQUIRED_OUTPUTS = [
    ("01_limiting_reagent_yield.py", ARTICLE_DIR / "outputs" / "tables" / "limiting_reagent_yield.csv"),
    ("02_solution_titration_gas.py", ARTICLE_DIR / "outputs" / "tables" / "solution_titration_gas.csv"),
    ("03_empirical_formula_combustion.py", ARTICLE_DIR / "outputs" / "tables" / "empirical_formula_combustion.csv"),
    ("04_reaction_extent_balances.py", ARTICLE_DIR / "outputs" / "tables" / "reaction_extent_balances.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    limiting = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "limiting_reagent_yield.csv").round(6)
    titration = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "titration_equivalence.csv").round(6)
    gas = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "gas_stoichiometry.csv").round(6)
    empirical = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "empirical_formula_ratios.csv").round(6)
    combustion = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "combustion_analysis.csv").round(6)
    extent = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "reaction_extent_balances.csv").round(6)

    report = [
        "# Stoichiometry and the Quantitative Language of Reactions",
        "",
        "This report was generated from simplified educational stoichiometry data.",
        "",
        "## Limiting Reagent and Yield",
        "",
        dataframe_to_markdown(limiting),
        "",
        "## Titration Equivalence",
        "",
        dataframe_to_markdown(titration),
        "",
        "## Gas Stoichiometry",
        "",
        dataframe_to_markdown(gas),
        "",
        "## Empirical Formula Ratios",
        "",
        dataframe_to_markdown(empirical),
        "",
        "## Combustion Analysis",
        "",
        dataframe_to_markdown(combustion),
        "",
        "## Reaction Extent Balances",
        "",
        dataframe_to_markdown(extent),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real stoichiometry work requires validated equations, units, purity corrections, uncertainty analysis, safety review, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
