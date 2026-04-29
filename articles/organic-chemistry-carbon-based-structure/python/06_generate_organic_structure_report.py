"""
Generate a report for Organic Chemistry and Carbon-Based Structure.

Run from article directory:
    python python/06_generate_organic_structure_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from organic_structure_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "organic_structure_report.md"

REQUIRED_OUTPUTS = [
    ("01_formula_descriptors.py", ARTICLE_DIR / "outputs" / "tables" / "formula_descriptors.csv"),
    ("02_molecular_graphs.py", ARTICLE_DIR / "outputs" / "tables" / "molecular_graphs.csv"),
    ("03_functional_groups_stereochemistry.py", ARTICLE_DIR / "outputs" / "tables" / "functional_groups_stereochemistry.csv"),
    ("04_structure_property_scaffold.py", ARTICLE_DIR / "outputs" / "tables" / "structure_property_scaffold.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    formula = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "formula_descriptors_only.csv").round(6)
    hybrid = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "hybridization_summary.csv")
    graph = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "molecular_graph_summary.csv").round(6)
    groups = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "functional_group_summary.csv")
    stereo = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "stereochemistry_summary.csv")
    property_table = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "structure_property_scaffold_only.csv")
    conformers = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "conformer_populations.csv").round(6)

    report = [
        "# Organic Chemistry and Carbon-Based Structure",
        "",
        "This report was generated from simplified educational organic-structure data.",
        "",
        "## Formula Descriptors",
        "",
        dataframe_to_markdown(formula),
        "",
        "## Carbon Hybridization Summary",
        "",
        dataframe_to_markdown(hybrid),
        "",
        "## Molecular Graph Summary",
        "",
        dataframe_to_markdown(graph),
        "",
        "## Functional Group Summary",
        "",
        dataframe_to_markdown(groups),
        "",
        "## Stereochemistry Summary",
        "",
        dataframe_to_markdown(stereo),
        "",
        "## Structure-Property Scaffold",
        "",
        dataframe_to_markdown(property_table),
        "",
        "## Conformer Populations",
        "",
        dataframe_to_markdown(conformers),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real organic-structure modeling requires validated structures, stereochemical specification, atom typing, aromaticity models, protonation-state analysis, conformational sampling, data provenance, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
