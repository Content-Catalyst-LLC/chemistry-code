"""
Generate a report for Equilibrium and the Dynamics of Reversible Systems.

Run from article directory:
    python python/06_generate_equilibrium_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from equilibrium_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "equilibrium_report.md"

REQUIRED_OUTPUTS = [
    ("01_reaction_quotient_free_energy.py", ARTICLE_DIR / "outputs" / "tables" / "reaction_quotient_free_energy.csv"),
    ("02_equilibrium_solver.py", ARTICLE_DIR / "outputs" / "tables" / "equilibrium_solver.csv"),
    ("03_reversible_dynamics.py", ARTICLE_DIR / "outputs" / "tables" / "reversible_dynamics.csv"),
    ("04_vant_hoff_solubility_activity.py", ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_solubility_activity.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    q_table = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "reaction_quotient_free_energy.csv").round(6)
    solver = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "equilibrium_solver.csv").round(6)
    dynamics = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "reversible_dynamics.csv").round(6)
    vant = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_fit.csv").round(6)
    solubility = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "solubility_product.csv").round(10)
    activity = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "activity_scaffold.csv").round(6)

    report = [
        "# Equilibrium and the Dynamics of Reversible Systems",
        "",
        "This report was generated from simplified educational equilibrium data.",
        "",
        "## Reaction Quotient and Free Energy",
        "",
        dataframe_to_markdown(q_table),
        "",
        "## Simple Equilibrium Solver",
        "",
        dataframe_to_markdown(solver),
        "",
        "## Reversible Dynamics Trajectory",
        "",
        dataframe_to_markdown(dynamics.head(20)),
        "",
        "## van 't Hoff Fit",
        "",
        dataframe_to_markdown(vant),
        "",
        "## Solubility Product Analysis",
        "",
        dataframe_to_markdown(solubility),
        "",
        "## Activity Scaffold",
        "",
        dataframe_to_markdown(activity),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real equilibrium modeling requires evaluated constants, clear standard states, temperature control, activity corrections, phase specification, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
