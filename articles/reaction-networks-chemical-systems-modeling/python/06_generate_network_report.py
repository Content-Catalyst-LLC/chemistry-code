"""
Generate a report for Reaction Networks and Chemical Systems Modeling.

Run from article directory:
    python python/06_generate_network_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from reaction_network_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "reaction_network_report.md"

REQUIRED_OUTPUTS = [
    ("01_stoichiometric_matrix.py", ARTICLE_DIR / "outputs" / "tables" / "stoichiometric_matrix.csv"),
    ("02_network_ode_simulation.py", ARTICLE_DIR / "outputs" / "tables" / "network_ode_simulation.csv"),
    ("03_parallel_branching_selectivity.py", ARTICLE_DIR / "outputs" / "tables" / "parallel_branching_selectivity.csv"),
    ("04_flux_sensitivity_fitting.py", ARTICLE_DIR / "outputs" / "tables" / "flux_sensitivity_fitting.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    stoich = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "stoichiometric_matrix.csv")
    simulation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "network_ode_simulation.csv").round(6)
    parallel = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "parallel_selectivity.csv").round(6)
    branching = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "branching_outcomes.csv").round(6)
    flux = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "flux_table.csv").round(6)
    sensitivity = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "sensitivity_analysis.csv").round(6)
    fit = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "simple_parameter_fit.csv").round(6)

    report = [
        "# Reaction Networks and Chemical Systems Modeling",
        "",
        "This report was generated from simplified educational reaction-network data.",
        "",
        "## Stoichiometric Matrix",
        "",
        dataframe_to_markdown(stoich),
        "",
        "## Network ODE Simulation",
        "",
        dataframe_to_markdown(simulation.head(20)),
        "",
        "## Parallel Selectivity",
        "",
        dataframe_to_markdown(parallel),
        "",
        "## Branching Outcomes",
        "",
        dataframe_to_markdown(branching),
        "",
        "## Flux Table",
        "",
        dataframe_to_markdown(flux),
        "",
        "## Sensitivity Analysis",
        "",
        dataframe_to_markdown(sensitivity),
        "",
        "## Simple Parameter Fit",
        "",
        dataframe_to_markdown(fit),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real reaction-network modeling requires validated mechanisms, thermodynamic consistency checks, solver diagnostics, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
