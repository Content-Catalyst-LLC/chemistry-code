"""
Generate a report for Computational Chemistry and Molecular Modeling.

Run from article directory:
    python python/06_generate_computational_chemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from computational_chemistry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "computational_chemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_molecular_descriptors.py", ARTICLE_DIR / "outputs" / "tables" / "molecular_descriptors.csv"),
    ("02_conformer_boltzmann.py", ARTICLE_DIR / "outputs" / "tables" / "conformer_boltzmann.csv"),
    ("03_potentials_similarity.py", ARTICLE_DIR / "outputs" / "tables" / "potentials_similarity.csv"),
    ("04_reaction_energy_modeling.py", ARTICLE_DIR / "outputs" / "tables" / "reaction_energy_modeling.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    descriptors = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "descriptor_table.csv").round(6)
    graphs = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "graph_table.csv").round(6)
    conformers = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "conformer_boltzmann.csv").round(6)
    lj = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "lennard_jones.csv").round(6)
    tanimoto = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "tanimoto_similarity.csv").round(6)
    rxn = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "reaction_energy_table.csv").round(6)
    md = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "toy_md_step.csv").round(6)

    report = [
        "# Computational Chemistry and Molecular Modeling",
        "",
        "This report was generated from simplified educational computational chemistry data.",
        "",
        "## Molecular Descriptors",
        "",
        dataframe_to_markdown(descriptors),
        "",
        "## Molecular Graphs",
        "",
        dataframe_to_markdown(graphs),
        "",
        "## Conformer Boltzmann Populations",
        "",
        dataframe_to_markdown(conformers),
        "",
        "## Lennard-Jones Potential",
        "",
        dataframe_to_markdown(lj),
        "",
        "## Tanimoto Similarity",
        "",
        dataframe_to_markdown(tanimoto),
        "",
        "## Reaction Energy Table",
        "",
        dataframe_to_markdown(rxn),
        "",
        "## Toy Molecular Dynamics Step",
        "",
        dataframe_to_markdown(md),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real computational chemistry requires validated structures, appropriate methods, basis sets or force fields, sampling checks, convergence diagnostics, uncertainty analysis, benchmarking, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))
    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
