"""
Run all analytical chemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_calibration_lod_loq.py",
    "02_precision_recovery_qc.py",
    "03_chromatography_spectroscopy.py",
    "04_spectral_matching_reporting.py",
    "05_provenance_manifest.py",
    "06_generate_analytical_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
