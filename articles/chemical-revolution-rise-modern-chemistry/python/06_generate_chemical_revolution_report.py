"""
Generate a report for The Chemical Revolution and the Rise of Modern Chemistry.

Run from article directory:
    python python/06_generate_chemical_revolution_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from chemical_revolution_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "chemical_revolution_report.md"

REQUIRED_OUTPUTS = [
    ("01_mass_conservation.py", ARTICLE_DIR / "outputs" / "tables" / "mass_conservation.csv"),
    ("02_oxidation_mass_gain.py", ARTICLE_DIR / "outputs" / "tables" / "oxidation_mass_gain.csv"),
    ("03_combustion_stoichiometry.py", ARTICLE_DIR / "outputs" / "tables" / "combustion_stoichiometry.csv"),
    ("04_nomenclature_mapping.py", ARTICLE_DIR / "outputs" / "tables" / "nomenclature_mapping.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    mass = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "mass_conservation.csv").round(5)
    oxidation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "oxidation_mass_gain.csv").round(5)
    combustion = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "combustion_stoichiometry.csv").round(5)
    nomenclature = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "nomenclature_mapping.csv")

    report = [
        "# The Chemical Revolution and the Rise of Modern Chemistry",
        "",
        "This report was generated from synthetic educational chemistry-history data.",
        "",
        "## Conservation of Mass",
        "",
        dataframe_to_markdown(mass),
        "",
        "## Oxidation Mass Gain",
        "",
        dataframe_to_markdown(oxidation[["metal", "oxide_name", "oxide_mass_g", "oxygen_mass_fraction", "mass_gain_percent"]]),
        "",
        "## Combustion Stoichiometry",
        "",
        dataframe_to_markdown(combustion[["reaction", "carbon_mass_g", "oxygen_mass_required_g", "carbon_dioxide_mass_g", "mass_balance_difference_g"]]),
        "",
        "## Nomenclature Mapping",
        "",
        dataframe_to_markdown(nomenclature),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. They illustrate quantitative ideas associated with the Chemical Revolution but do not reconstruct actual eighteenth-century experiments.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
