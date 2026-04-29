"""
Run all molecular dynamics Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_velocity_verlet.py",
    "02_potentials.py",
    "03_trajectory_analysis.py",
    "04_rdf_ensemble_metadata.py",
    "05_provenance_manifest.py",
    "06_generate_md_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
