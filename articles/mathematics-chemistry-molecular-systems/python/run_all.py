"""
Run all mathematical chemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_stoichiometry_and_ph.py",
    "02_kinetics_and_thermodynamics.py",
    "03_molecular_geometry.py",
    "04_linear_algebra_and_uncertainty.py",
    "05_provenance_manifest.py",
    "06_generate_math_chemistry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
