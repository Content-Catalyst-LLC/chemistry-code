"""
Generate a report for Mathematics for Chemistry and Molecular Systems.

Run from article directory:
    python python/06_generate_math_chemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from math_chemistry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "mathematics_chemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_stoichiometry_and_ph.py", ARTICLE_DIR / "outputs" / "tables" / "stoichiometry_and_ph.csv"),
    ("02_kinetics_and_thermodynamics.py", ARTICLE_DIR / "outputs" / "tables" / "kinetics_and_thermodynamics.csv"),
    ("03_molecular_geometry.py", ARTICLE_DIR / "outputs" / "tables" / "molecular_distances.csv"),
    ("04_linear_algebra_and_uncertainty.py", ARTICLE_DIR / "outputs" / "tables" / "linear_algebra_and_uncertainty.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    distances = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "molecular_distances.csv").round(6)
    kinetics = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "kinetics_trajectories.csv").round(6)
    thermo = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "thermodynamics_equilibrium.csv").round(6)
    eigen = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "matrix_eigenvalues.csv").round(6)
    uncertainty = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "uncertainty_summary.csv").round(6)

    report = [
        "# Mathematics for Chemistry and Molecular Systems",
        "",
        "This report was generated from synthetic educational mathematical chemistry data.",
        "",
        "## Molecular Distances",
        "",
        dataframe_to_markdown(distances),
        "",
        "## Kinetics",
        "",
        dataframe_to_markdown(kinetics.head(12)),
        "",
        "## Thermodynamics",
        "",
        dataframe_to_markdown(thermo[["reaction", "delta_g_standard_kj_mol", "temperature_k", "equilibrium_constant_K"]]),
        "",
        "## Matrix Eigenvalues",
        "",
        dataframe_to_markdown(eigen),
        "",
        "## Uncertainty Summary",
        "",
        dataframe_to_markdown(uncertainty),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemistry requires chemically meaningful models, validated methods, clear units, uncertainty analysis, and professional review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
