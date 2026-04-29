"""
Generate a report for Molecular Dynamics and Chemical Simulation.

Run from article directory:
    python python/06_generate_md_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from molecular_dynamics_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "molecular_dynamics_report.md"

REQUIRED_OUTPUTS = [
    ("01_velocity_verlet.py", ARTICLE_DIR / "outputs" / "tables" / "velocity_verlet.csv"),
    ("02_potentials.py", ARTICLE_DIR / "outputs" / "tables" / "potentials.csv"),
    ("03_trajectory_analysis.py", ARTICLE_DIR / "outputs" / "tables" / "trajectory_analysis.csv"),
    ("04_rdf_ensemble_metadata.py", ARTICLE_DIR / "outputs" / "tables" / "rdf_ensemble_metadata.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    verlet = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "velocity_verlet.csv").round(6)
    lj = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "lennard_jones.csv").round(6)
    coulomb = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "coulomb_energy.csv").round(6)
    traj = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "trajectory_analysis.csv").round(6)
    rdf = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "rdf_histogram.csv").round(6)
    ensemble = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "ensemble_metadata.csv")
    summary = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "trajectory_summary_processed.csv")

    report = [
        "# Molecular Dynamics and Chemical Simulation",
        "",
        "This report was generated from simplified educational molecular dynamics data.",
        "",
        "## Velocity Verlet Update",
        "",
        dataframe_to_markdown(verlet),
        "",
        "## Lennard-Jones Potential",
        "",
        dataframe_to_markdown(lj),
        "",
        "## Coulomb Energy",
        "",
        dataframe_to_markdown(coulomb),
        "",
        "## Trajectory Mean-Squared Displacement",
        "",
        dataframe_to_markdown(traj),
        "",
        "## RDF-Like Histogram",
        "",
        dataframe_to_markdown(rdf),
        "",
        "## Ensemble Metadata",
        "",
        dataframe_to_markdown(ensemble),
        "",
        "## Trajectory Summary Metadata",
        "",
        dataframe_to_markdown(summary),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real molecular dynamics requires validated force fields, careful system preparation, sufficient sampling, convergence checks, uncertainty analysis, expert review, and comparison with experimental or benchmark evidence where possible.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))
    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
