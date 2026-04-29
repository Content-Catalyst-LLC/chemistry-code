"""
Run all Python chemistry workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_calibration_curve.py",
    "02_kinetics_analysis.py",
    "03_uncertainty_qc.py",
    "04_simulation_workflow.py",
    "05_provenance_manifest.py",
    "06_generate_python_chemistry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
