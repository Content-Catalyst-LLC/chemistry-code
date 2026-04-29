"""
Generate a report for Chemical Biology and Molecular Intervention in Living Systems.

Run from article directory:
    python python/06_generate_chemical_biology_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from chemical_biology_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "chemical_biology_report.md"

REQUIRED_OUTPUTS = [
    ("01_dose_response.py", ARTICLE_DIR / "outputs" / "tables" / "dose_response.csv"),
    ("02_target_engagement_probe_quality.py", ARTICLE_DIR / "outputs" / "tables" / "target_engagement_probe_quality.csv"),
    ("03_chemoproteomics_selectivity.py", ARTICLE_DIR / "outputs" / "tables" / "chemoproteomics_selectivity.csv"),
    ("04_perturbation_networks.py", ARTICLE_DIR / "outputs" / "tables" / "perturbation_networks.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    dose = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "dose_response_only.csv").round(6)
    occupancy = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "occupancy.csv").round(6)
    engagement = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "target_engagement.csv").round(6)
    probes = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "probe_quality.csv").round(6)
    chemoproteomics = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "chemoproteomics_competition_summary.csv").round(6)
    selectivity = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "selectivity_summary.csv").round(6)
    perturbation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "perturbation_vector.csv").round(6)
    network = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "network_summary.csv").round(6)

    report = [
        "# Chemical Biology and Molecular Intervention in Living Systems",
        "",
        "This report was generated from simplified educational chemical-biology data.",
        "",
        "## Dose Response",
        "",
        dataframe_to_markdown(dose),
        "",
        "## Target Occupancy",
        "",
        dataframe_to_markdown(occupancy),
        "",
        "## Target Engagement",
        "",
        dataframe_to_markdown(engagement),
        "",
        "## Probe Quality",
        "",
        dataframe_to_markdown(probes),
        "",
        "## Chemoproteomics Competition",
        "",
        dataframe_to_markdown(chemoproteomics),
        "",
        "## Selectivity Summary",
        "",
        dataframe_to_markdown(selectivity),
        "",
        "## Perturbation Vector",
        "",
        dataframe_to_markdown(perturbation),
        "",
        "## Network Summary",
        "",
        dataframe_to_markdown(network),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemical biology requires validated probes, target engagement evidence, assay controls, biological context, off-target assessment, biosafety review, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))
    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
