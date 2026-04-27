"""
Run all introductory chemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_moles_molarity_dilution.py",
    "02_first_order_kinetics.py",
    "03_beer_lambert_calibration.py",
    "04_ph_calculations.py",
    "05_provenance_manifest.py",
    "06_generate_chemistry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
