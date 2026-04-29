"""
Generate a report for Catalysis and the Control of Chemical Pathways.

Run from article directory:
    python python/06_generate_catalysis_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from catalysis_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "catalysis_report.md"

REQUIRED_OUTPUTS = [
    ("01_barrier_rate_enhancement.py", ARTICLE_DIR / "outputs" / "tables" / "barrier_rate_enhancement.csv"),
    ("02_turnover_metrics.py", ARTICLE_DIR / "outputs" / "tables" / "turnover_metrics.csv"),
    ("03_adsorption_surface_rates.py", ARTICLE_DIR / "outputs" / "tables" / "adsorption_surface_rates.csv"),
    ("04_catalytic_cycle_deactivation.py", ARTICLE_DIR / "outputs" / "tables" / "catalytic_cycle_deactivation.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    barrier = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "barrier_rate_enhancement.csv").round(6)
    turnover = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "turnover_metrics.csv").round(8)
    adsorption = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "adsorption_surface_rates_only.csv").round(6)
    enzyme = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "michaelis_menten_rates.csv").round(6)
    cycle = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "catalytic_cycle_simulation.csv").round(6)
    deactivation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "deactivation_profiles.csv").round(6)

    report = [
        "# Catalysis and the Control of Chemical Pathways",
        "",
        "This report was generated from simplified educational catalysis data.",
        "",
        "## Barrier Lowering and Rate Enhancement",
        "",
        dataframe_to_markdown(barrier),
        "",
        "## Turnover Metrics",
        "",
        dataframe_to_markdown(turnover),
        "",
        "## Langmuir Surface Rates",
        "",
        dataframe_to_markdown(adsorption),
        "",
        "## Michaelis-Menten Rates",
        "",
        dataframe_to_markdown(enzyme),
        "",
        "## Catalytic Cycle Scaffold",
        "",
        dataframe_to_markdown(cycle.head(20)),
        "",
        "## Deactivation Profiles",
        "",
        dataframe_to_markdown(deactivation.head(20)),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real catalytic analysis requires validated kinetics, catalyst characterization, transport checks, deactivation assessment, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
