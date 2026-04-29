"""
Run all cheminformatics Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_descriptors_graphs.py",
    "02_fingerprints_similarity.py",
    "03_assay_standardization.py",
    "04_splits_applicability_modeling.py",
    "05_provenance_manifest.py",
    "06_generate_cheminformatics_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
