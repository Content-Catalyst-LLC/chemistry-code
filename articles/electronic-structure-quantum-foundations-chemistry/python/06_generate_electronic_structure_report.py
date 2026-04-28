"""
Generate a report for Electronic Structure and the Quantum Foundations of Chemistry.

Run from article directory:
    python python/06_generate_electronic_structure_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from electronic_structure_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "electronic_structure_report.md"

REQUIRED_OUTPUTS = [
    ("01_hydrogen_energy_levels.py", ARTICLE_DIR / "outputs" / "tables" / "hydrogen_energy_levels_and_transitions.csv"),
    ("02_orbital_capacity_and_configuration.py", ARTICLE_DIR / "outputs" / "tables" / "orbital_capacity_and_configuration.csv"),
    ("03_particle_in_box.py", ARTICLE_DIR / "outputs" / "tables" / "particle_in_box_levels.csv"),
    ("04_hamiltonian_eigenproblem.py", ARTICLE_DIR / "outputs" / "tables" / "hamiltonian_eigenvalues.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    levels = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "hydrogen_energy_levels.csv").round(6)
    transitions = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "hydrogen_transitions.csv").round(3)
    orbitals = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "orbital_capacities.csv")
    zeff = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "effective_nuclear_charge.csv").round(3)
    box = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "particle_in_box_levels.csv").round(6)
    eigenvalues = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "hamiltonian_eigenvalues.csv").round(6)

    report = [
        "# Electronic Structure and the Quantum Foundations of Chemistry",
        "",
        "This report was generated from simplified educational electronic-structure data.",
        "",
        "## Hydrogen Energy Levels",
        "",
        dataframe_to_markdown(levels),
        "",
        "## Transitions to n=1",
        "",
        dataframe_to_markdown(transitions),
        "",
        "## Orbital Capacities",
        "",
        dataframe_to_markdown(orbitals),
        "",
        "## Effective Nuclear Charge",
        "",
        dataframe_to_markdown(zeff),
        "",
        "## Particle-in-a-Box Levels",
        "",
        dataframe_to_markdown(box.head(12)),
        "",
        "## Hamiltonian Eigenvalues",
        "",
        dataframe_to_markdown(eigenvalues),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real electronic-structure chemistry requires validated models, documented assumptions, convergence checks, uncertainty analysis, and expert review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
