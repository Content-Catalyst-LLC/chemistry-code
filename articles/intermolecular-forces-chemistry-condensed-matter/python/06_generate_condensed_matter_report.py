"""
Generate a report for Intermolecular Forces and the Chemistry of Condensed Matter.

Run from article directory:
    python python/06_generate_condensed_matter_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from condensed_matter_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "intermolecular_forces_report.md"

REQUIRED_OUTPUTS = [
    ("01_lennard_jones_potential.py", ARTICLE_DIR / "outputs" / "tables" / "lennard_jones_minima.csv"),
    ("02_vapor_pressure_fit.py", ARTICLE_DIR / "outputs" / "tables" / "vapor_pressure_fit.csv"),
    ("03_radial_distribution_scaffold.py", ARTICLE_DIR / "outputs" / "tables" / "radial_distribution_scaffold.csv"),
    ("04_phase_property_summary.py", ARTICLE_DIR / "outputs" / "tables" / "phase_property_summary.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    minima = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "lennard_jones_minima.csv").round(6)
    vapor = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "vapor_pressure_fit.csv").round(6)
    rdf = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "radial_distribution_scaffold.csv")
    phase = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "phase_property_summary.csv")
    surface = pd.read_csv(ARTICLE_DIR / "data" / "surface_tension_sample.csv")

    report = [
        "# Intermolecular Forces and the Chemistry of Condensed Matter",
        "",
        "This report was generated from simplified educational condensed-matter chemistry data.",
        "",
        "## Lennard-Jones Potential Minima",
        "",
        dataframe_to_markdown(minima),
        "",
        "## Vapor Pressure Fit",
        "",
        dataframe_to_markdown(vapor),
        "",
        "## Radial Distribution Scaffold",
        "",
        dataframe_to_markdown(rdf),
        "",
        "## Phase Property Summary",
        "",
        dataframe_to_markdown(phase.head(20)),
        "",
        "## Surface Tension Sample",
        "",
        dataframe_to_markdown(surface),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real condensed-matter chemistry requires validated interaction models, reference data, unit conventions, uncertainty analysis, and expert review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
