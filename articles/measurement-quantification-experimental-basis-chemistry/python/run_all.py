"""
Run all measurement and quantification Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_mass_volume_concentration.py",
    "02_calibration_curve.py",
    "03_replicate_uncertainty.py",
    "04_dilution_workflow.py",
    "05_provenance_manifest.py",
    "06_generate_measurement_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
