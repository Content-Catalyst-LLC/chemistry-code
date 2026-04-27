"""
Generate a report for Measurement, Quantification, and the Experimental Basis of Chemistry.

Run from article directory:
    python python/06_generate_measurement_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from measurement_quantification_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "measurement_quantification_report.md"

REQUIRED_OUTPUTS = [
    ("01_mass_volume_concentration.py", ARTICLE_DIR / "outputs" / "tables" / "mass_volume_concentration.csv"),
    ("02_calibration_curve.py", ARTICLE_DIR / "outputs" / "tables" / "calibration_estimates.csv"),
    ("03_replicate_uncertainty.py", ARTICLE_DIR / "outputs" / "tables" / "replicate_uncertainty.csv"),
    ("04_dilution_workflow.py", ARTICLE_DIR / "outputs" / "tables" / "dilution_plan_calculated.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    mvc = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "mass_volume_concentration.csv").round(6)
    calibration = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "calibration_estimates.csv").round(6)
    uncertainty = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "replicate_uncertainty.csv").round(8)
    dilution = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "dilution_plan_calculated.csv").round(6)

    report = [
        "# Measurement, Quantification, and the Experimental Basis of Chemistry",
        "",
        "This report was generated from synthetic educational chemistry measurement data.",
        "",
        "## Mass, Amount of Substance, and Concentration",
        "",
        dataframe_to_markdown(mvc[["sample", "substance", "moles", "concentration_mol_l"]]),
        "",
        "## Calibration Estimates",
        "",
        dataframe_to_markdown(calibration[["unknown_id", "instrument_response", "estimated_concentration_mol_l"]]),
        "",
        "## Replicate Precision and Uncertainty",
        "",
        dataframe_to_markdown(uncertainty),
        "",
        "## Dilution Planning",
        "",
        dataframe_to_markdown(dilution[["solution", "stock_volume_ml", "diluent_volume_ml", "final_volume_ml"]]),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemical measurement requires calibration, uncertainty analysis, validated methods, safety procedures, appropriate equipment, and professional review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
