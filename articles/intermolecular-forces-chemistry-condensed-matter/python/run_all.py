"""
Run all intermolecular-forces Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_lennard_jones_potential.py",
    "02_vapor_pressure_fit.py",
    "03_radial_distribution_scaffold.py",
    "04_phase_property_summary.py",
    "05_provenance_manifest.py",
    "06_generate_condensed_matter_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
