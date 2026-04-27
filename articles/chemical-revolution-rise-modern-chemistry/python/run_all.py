"""
Run all Chemical Revolution Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_mass_conservation.py",
    "02_oxidation_mass_gain.py",
    "03_combustion_stoichiometry.py",
    "04_nomenclature_mapping.py",
    "05_provenance_manifest.py",
    "06_generate_chemical_revolution_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
