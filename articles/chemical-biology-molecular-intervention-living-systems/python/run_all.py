"""
Run all chemical biology Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_dose_response.py",
    "02_target_engagement_probe_quality.py",
    "03_chemoproteomics_selectivity.py",
    "04_perturbation_networks.py",
    "05_provenance_manifest.py",
    "06_generate_chemical_biology_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
