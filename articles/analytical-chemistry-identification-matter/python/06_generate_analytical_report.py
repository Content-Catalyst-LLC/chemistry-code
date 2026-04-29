"""
Generate a report for Analytical Chemistry and the Identification of Matter.

Run from article directory:
    python python/06_generate_analytical_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from analytical_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "analytical_report.md"

REQUIRED_OUTPUTS = [
    ("01_calibration_lod_loq.py", ARTICLE_DIR / "outputs" / "tables" / "calibration_lod_loq.csv"),
    ("02_precision_recovery_qc.py", ARTICLE_DIR / "outputs" / "tables" / "precision_recovery_qc.csv"),
    ("03_chromatography_spectroscopy.py", ARTICLE_DIR / "outputs" / "tables" / "chromatography_spectroscopy.csv"),
    ("04_spectral_matching_reporting.py", ARTICLE_DIR / "outputs" / "tables" / "spectral_matching_reporting.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    calibration = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "calibration_model.csv").round(8)
    unknowns = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "unknown_concentrations.csv").round(8)
    precision = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "precision_summary.csv").round(6)
    recovery = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "spike_recovery_summary.csv").round(6)
    chrom = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "chromatographic_resolution.csv").round(6)
    beer = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "beer_lambert_quantification.csv").round(10)
    spectral = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "spectral_matching_reporting.csv").round(8)

    report = [
        "# Analytical Chemistry and the Identification of Matter",
        "",
        "This report was generated from simplified educational analytical chemistry data.",
        "",
        "## Calibration Model",
        "",
        dataframe_to_markdown(calibration),
        "",
        "## Unknown Concentrations",
        "",
        dataframe_to_markdown(unknowns),
        "",
        "## Precision Summary",
        "",
        dataframe_to_markdown(precision),
        "",
        "## Spike Recovery Summary",
        "",
        dataframe_to_markdown(recovery),
        "",
        "## Chromatographic Resolution",
        "",
        dataframe_to_markdown(chrom),
        "",
        "## Beer-Lambert Quantification",
        "",
        dataframe_to_markdown(beer),
        "",
        "## Spectral Matching",
        "",
        dataframe_to_markdown(spectral),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real analytical chemistry requires validated methods, matrix assessment, calibration design, reference materials, uncertainty analysis, quality-control rules, trained personnel, and fit-for-purpose interpretation.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
