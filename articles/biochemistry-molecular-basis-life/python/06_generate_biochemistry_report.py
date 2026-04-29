"""
Generate a report for Biochemistry and the Molecular Basis of Life.

Run from article directory:
    python python/06_generate_biochemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from biochemistry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "biochemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_enzyme_kinetics.py", ARTICLE_DIR / "outputs" / "tables" / "enzyme_kinetics.csv"),
    ("02_binding_occupancy.py", ARTICLE_DIR / "outputs" / "tables" / "binding_occupancy.csv"),
    ("03_sequence_composition.py", ARTICLE_DIR / "outputs" / "tables" / "sequence_composition.csv"),
    ("04_metabolic_networks.py", ARTICLE_DIR / "outputs" / "tables" / "metabolic_networks.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    enzyme = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "enzyme_kinetics.csv").round(6)
    binding = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "binding_occupancy.csv").round(6)
    sequence = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "sequence_composition_only.csv").round(6)
    biomolecule = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "biomolecule_class_descriptors.csv")
    flux = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "flux_balance.csv").round(6)
    network = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "network_summary.csv")
    energy = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "biochemical_free_energy.csv").round(6)

    report = [
        "# Biochemistry and the Molecular Basis of Life",
        "",
        "This report was generated from simplified educational biochemical data.",
        "",
        "## Enzyme Kinetics",
        "",
        dataframe_to_markdown(enzyme),
        "",
        "## Binding Occupancy",
        "",
        dataframe_to_markdown(binding),
        "",
        "## Sequence Composition",
        "",
        dataframe_to_markdown(sequence),
        "",
        "## Biomolecule Class Descriptors",
        "",
        dataframe_to_markdown(biomolecule),
        "",
        "## Flux Balance",
        "",
        dataframe_to_markdown(flux),
        "",
        "## Network Summary",
        "",
        dataframe_to_markdown(network),
        "",
        "## Biochemical Free Energy",
        "",
        dataframe_to_markdown(energy),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real biochemistry requires validated assays, biological context, experimental controls, uncertainty analysis, safety review, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
