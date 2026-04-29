"""
Generate a report for Python for Chemistry, Simulation, and Laboratory Data.

Run from article directory:
    python python/06_generate_python_chemistry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from python_chemistry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "python_chemistry_report.md"

REQUIRED_OUTPUTS = [
    ("01_calibration_curve.py", ARTICLE_DIR / "outputs" / "tables" / "calibration_curve.csv"),
    ("02_kinetics_analysis.py", ARTICLE_DIR / "outputs" / "tables" / "kinetics_analysis.csv"),
    ("03_uncertainty_qc.py", ARTICLE_DIR / "outputs" / "tables" / "uncertainty_qc.csv"),
    ("04_simulation_workflow.py", ARTICLE_DIR / "outputs" / "tables" / "simulation_workflow.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    calibration = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "calibration_model.csv").round(6)
    unknowns = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "unknown_concentrations.csv").round(6)
    kinetics = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "first_order_kinetics.csv").round(6)
    arrhenius = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "arrhenius_transform.csv").round(6)
    replicate = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "replicate_summary.csv").round(6)
    simulation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "simulation_workflow.csv").round(6)

    report = [
        "# Python for Chemistry, Simulation, and Laboratory Data",
        "",
        "This report was generated from simplified educational chemical data.",
        "",
        "## Calibration Model",
        "",
        dataframe_to_markdown(calibration),
        "",
        "## Unknown Concentration Estimates",
        "",
        dataframe_to_markdown(unknowns),
        "",
        "## First-Order Kinetics",
        "",
        dataframe_to_markdown(kinetics),
        "",
        "## Arrhenius Transform",
        "",
        dataframe_to_markdown(arrhenius),
        "",
        "## Replicate Summary",
        "",
        dataframe_to_markdown(replicate),
        "",
        "## Simulation Workflow",
        "",
        dataframe_to_markdown(simulation),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemical analysis requires validated analytical methods, instrument qualification, calibration checks, uncertainty budgets, sample preparation records, quality-control standards, and expert interpretation.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))
    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
