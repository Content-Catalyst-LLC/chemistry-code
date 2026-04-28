"""
Run all atoms, elements, and periodic organization Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_element_features.py",
    "02_isotope_weighted_mass.py",
    "03_periodic_trends.py",
    "04_mole_and_composition.py",
    "05_provenance_manifest.py",
    "06_generate_periodic_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
