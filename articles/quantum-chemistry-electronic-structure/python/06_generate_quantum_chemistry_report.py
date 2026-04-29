"""
Generate a report for Quantum Chemistry and Electronic Structure.

Run from article directory:
    python python/06_generate_quantum_chemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from quantum_chemistry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "quantum_chemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_orbital_mixing.py", ARTICLE_DIR / "outputs" / "tables" / "orbital_mixing.csv"),
    ("02_density_huckel.py", ARTICLE_DIR / "outputs" / "tables" / "density_huckel.csv"),
    ("03_basis_spin_states.py", ARTICLE_DIR / "outputs" / "tables" / "basis_spin_states.csv"),
    ("04_excited_states_tst.py", ARTICLE_DIR / "outputs" / "tables" / "excited_states_tst.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    orbital = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "orbital_mixing.csv").round(6)
    density = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "electron_density.csv").round(6)
    huckel = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "huckel_levels.csv").round(6)
    basis = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "basis_convergence.csv").round(6)
    spin = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "spin_state_summary.csv").round(6)
    excited = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "excited_state_populations.csv").round(10)
    tst = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "transition_state_theory.csv")

    report = [
        "# Quantum Chemistry and Electronic Structure",
        "",
        "This report was generated from simplified educational quantum chemistry data.",
        "",
        "## Orbital Mixing",
        "",
        dataframe_to_markdown(orbital),
        "",
        "## Electron Density",
        "",
        dataframe_to_markdown(density),
        "",
        "## Hückel Energy Levels",
        "",
        dataframe_to_markdown(huckel),
        "",
        "## Basis-Set Convergence",
        "",
        dataframe_to_markdown(basis),
        "",
        "## Spin-State Summary",
        "",
        dataframe_to_markdown(spin),
        "",
        "## Excited-State Populations",
        "",
        dataframe_to_markdown(excited),
        "",
        "## Transition-State-Theory Rates",
        "",
        dataframe_to_markdown(tst),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real quantum chemistry requires validated structures, appropriate charge and spin, method and basis-set selection, convergence diagnostics, frequency checks, benchmark comparison, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))
    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
