"""
Generate a report for Physical Chemistry and the Chemical Interpretation of Matter.

Run from article directory:
    python python/06_generate_physical_chemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from physical_chemistry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "physical_chemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_thermodynamics_equilibrium.py", ARTICLE_DIR / "outputs" / "tables" / "thermodynamics_equilibrium.csv"),
    ("02_arrhenius_kinetics.py", ARTICLE_DIR / "outputs" / "tables" / "arrhenius_kinetics.csv"),
    ("03_boltzmann_diffusion.py", ARTICLE_DIR / "outputs" / "tables" / "boltzmann_diffusion.csv"),
    ("04_electrochemistry_transport.py", ARTICLE_DIR / "outputs" / "tables" / "electrochemistry_transport.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    thermo = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "thermodynamics_equilibrium.csv").round(6)
    arrhenius = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "arrhenius_kinetics.csv")
    boltzmann = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "boltzmann_populations.csv").round(8)
    diffusion = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "diffusion_profiles.csv").round(8)
    electro = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "electrochemistry_transport.csv").round(6)

    report = [
        "# Physical Chemistry and the Chemical Interpretation of Matter",
        "",
        "This report was generated from simplified educational physical chemistry data.",
        "",
        "## Thermodynamics and Equilibrium",
        "",
        dataframe_to_markdown(thermo),
        "",
        "## Arrhenius Kinetics",
        "",
        dataframe_to_markdown(arrhenius),
        "",
        "## Boltzmann Populations",
        "",
        dataframe_to_markdown(boltzmann),
        "",
        "## Diffusion Profiles",
        "",
        dataframe_to_markdown(diffusion.head(30)),
        "",
        "## Electrochemistry",
        "",
        dataframe_to_markdown(electro),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real physical chemistry requires validated models, units, calibrated measurements, solvent and activity assumptions, numerical diagnostics, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
