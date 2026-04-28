"""
Generate a report for Acids, Bases, and Proton Transfer.

Run from article directory:
    python python/06_generate_acid_base_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from acid_base_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "acid_base_report.md"

REQUIRED_OUTPUTS = [
    ("01_weak_acid_base_ph.py", ARTICLE_DIR / "outputs" / "tables" / "weak_acid_base_ph.csv"),
    ("02_buffer_henderson_hasselbalch.py", ARTICLE_DIR / "outputs" / "tables" / "buffer_henderson_hasselbalch.csv"),
    ("03_titration_curves.py", ARTICLE_DIR / "outputs" / "tables" / "titration_curves.csv"),
    ("04_speciation_polyprotic.py", ARTICLE_DIR / "outputs" / "tables" / "speciation_polyprotic.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    weak = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "weak_acid_base_ph.csv").round(6)
    buffer = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "buffer_henderson_hasselbalch.csv").round(6)
    titration = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "titration_curves.csv").round(6)
    mono = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "monoprotic_speciation.csv").round(6)
    poly = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "polyprotic_distribution.csv").round(6)

    report = [
        "# Acids, Bases, and Proton Transfer",
        "",
        "This report was generated from simplified educational acid-base chemistry data.",
        "",
        "## Weak Acid and Weak Base pH",
        "",
        dataframe_to_markdown(weak),
        "",
        "## Henderson-Hasselbalch Buffer Estimates",
        "",
        dataframe_to_markdown(buffer),
        "",
        "## Titration Curve Scaffold",
        "",
        dataframe_to_markdown(titration.head(20)),
        "",
        "## Monoprotic Speciation",
        "",
        dataframe_to_markdown(mono.head(20)),
        "",
        "## Polyprotic Distribution",
        "",
        dataframe_to_markdown(poly.head(20)),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real acid-base analysis requires temperature control, calibrated measurement, activity corrections when appropriate, ionic strength awareness, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
