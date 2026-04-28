"""
Run all periodic-classification Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_periodic_classification.py",
    "02_periodic_trends.py",
    "03_element_similarity.py",
    "04_atomic_weight_and_features.py",
    "05_provenance_manifest.py",
    "06_generate_periodic_classification_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
