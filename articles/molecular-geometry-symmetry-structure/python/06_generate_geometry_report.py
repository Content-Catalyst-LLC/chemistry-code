"""
Generate a report for Molecular Geometry, Symmetry, and Structure.

Run from article directory:
    python python/06_generate_geometry_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from geometry_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "molecular_geometry_report.md"

REQUIRED_OUTPUTS = [
    ("01_distance_matrix_and_angles.py", ARTICLE_DIR / "outputs" / "tables" / "distance_matrix_and_angles.csv"),
    ("02_centers_and_extents.py", ARTICLE_DIR / "outputs" / "tables" / "centers_and_extents.csv"),
    ("03_rotation_and_symmetry_operation.py", ARTICLE_DIR / "outputs" / "tables" / "rotation_and_symmetry_operation.csv"),
    ("04_conformer_rmsd_and_torsion.py", ARTICLE_DIR / "outputs" / "tables" / "conformer_rmsd_and_torsion.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    distances = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "bond_distances.csv").round(6)
    angles = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "bond_angles.csv").round(3)
    centers = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "centers_and_extents.csv").round(6)
    rotation = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "rotation_and_symmetry_operation.csv").round(6)
    rmsd = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "conformer_rmsd.csv").round(6)
    vsepr = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "vsepr_summary.csv")

    report = [
        "# Molecular Geometry, Symmetry, and Structure",
        "",
        "This report was generated from simplified educational molecular-geometry data.",
        "",
        "## Bond Distances",
        "",
        dataframe_to_markdown(distances),
        "",
        "## Bond Angles",
        "",
        dataframe_to_markdown(angles),
        "",
        "## Centers and Extents",
        "",
        dataframe_to_markdown(centers),
        "",
        "## Rotation Operation Example",
        "",
        dataframe_to_markdown(rotation),
        "",
        "## Conformer RMSD",
        "",
        dataframe_to_markdown(rmsd),
        "",
        "## VSEPR Summary",
        "",
        dataframe_to_markdown(vsepr),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real molecular structure work requires validated data, chemically meaningful models, experimental evidence, uncertainty analysis, and expert review.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
