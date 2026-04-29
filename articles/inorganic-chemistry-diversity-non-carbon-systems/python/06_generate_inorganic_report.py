"""
Generate a report for Inorganic Chemistry and the Diversity of Non-Carbon Systems.

Run from article directory:
    python python/06_generate_inorganic_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from inorganic_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "inorganic_report.md"

REQUIRED_OUTPUTS = [
    ("01_oxidation_states.py", ARTICLE_DIR / "outputs" / "tables" / "oxidation_states.csv"),
    ("02_coordination_ligands.py", ARTICLE_DIR / "outputs" / "tables" / "coordination_ligands.csv"),
    ("03_crystal_field_magnetism.py", ARTICLE_DIR / "outputs" / "tables" / "crystal_field_magnetism.csv"),
    ("04_ionic_materials_descriptors.py", ARTICLE_DIR / "outputs" / "tables" / "ionic_materials_descriptors.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    oxidation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "oxidation_states.csv").round(6)
    coordination = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "coordination_summary.csv")
    ligands = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "ligand_summary.csv")
    crystal = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "crystal_field_magnetism.csv").round(6)
    ionic = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "ionic_solid_descriptors.csv").round(6)
    perov = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "perovskite_tolerance.csv").round(6)
    materials = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "material_descriptor_table.csv").round(6)

    report = [
        "# Inorganic Chemistry and the Diversity of Non-Carbon Systems",
        "",
        "This report was generated from simplified educational inorganic-chemistry data.",
        "",
        "## Oxidation-State Accounting",
        "",
        dataframe_to_markdown(oxidation),
        "",
        "## Coordination Summary",
        "",
        dataframe_to_markdown(coordination),
        "",
        "## Ligand Summary",
        "",
        dataframe_to_markdown(ligands),
        "",
        "## Crystal Field and Magnetism",
        "",
        dataframe_to_markdown(crystal),
        "",
        "## Ionic Solid Descriptors",
        "",
        dataframe_to_markdown(ionic),
        "",
        "## Perovskite Tolerance Factors",
        "",
        dataframe_to_markdown(perov),
        "",
        "## Materials Descriptor Table",
        "",
        dataframe_to_markdown(materials),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real inorganic chemistry requires validated structures, spectroscopy, oxidation-state evidence, spin-state analysis, phase characterization, safety review, environmental context, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
