"""
Generate a report for Chemical Metrology, Standards, and Reference Materials.

Run from article directory:
    python python/06_generate_metrology_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from metrology_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "chemical_metrology_report.md"

REQUIRED_OUTPUTS = [
    ("01_uncertainty_budget.py", ARTICLE_DIR / "outputs" / "tables" / "uncertainty_budget_summary.csv"),
    ("02_reference_material_summary.py", ARTICLE_DIR / "outputs" / "tables" / "reference_material_summary.csv"),
    ("03_traceability_chain.py", ARTICLE_DIR / "outputs" / "tables" / "traceability_chain_summary.csv"),
    ("04_interlaboratory_comparison.py", ARTICLE_DIR / "outputs" / "tables" / "interlaboratory_comparison.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    uncertainty = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "uncertainty_budget_summary.csv").round(6)
    materials = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "reference_material_summary.csv").round(4)
    chain = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "traceability_chain_summary.csv").round(5)
    interlab = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "interlaboratory_comparison.csv").round(4)

    report = [
        "# Chemical Metrology, Standards, and Reference Materials",
        "",
        "This report was generated from synthetic educational chemical metrology data.",
        "",
        "## Uncertainty Budget",
        "",
        dataframe_to_markdown(uncertainty),
        "",
        "## Reference Material Summary",
        "",
        dataframe_to_markdown(materials[["material_id", "material_type", "measurand", "certified_value", "expanded_uncertainty", "unit", "relative_expanded_uncertainty_percent"]]),
        "",
        "## Traceability Chain",
        "",
        dataframe_to_markdown(chain[["step_order", "chain_level", "reference", "expanded_uncertainty", "cumulative_root_sum_square_uncertainty"]]),
        "",
        "## Interlaboratory Comparison",
        "",
        dataframe_to_markdown(interlab[["laboratory", "lab_result", "bias", "normalized_error_en", "acceptable_by_abs_en_le_1"]]),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real chemical metrology requires validated methods, appropriate reference materials, traceability documentation, uncertainty analysis, and professional review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
