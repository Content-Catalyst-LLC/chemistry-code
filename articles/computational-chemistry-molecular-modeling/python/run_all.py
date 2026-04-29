"""
Run all computational chemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_molecular_descriptors.py",
    "02_conformer_boltzmann.py",
    "03_potentials_similarity.py",
    "04_reaction_energy_modeling.py",
    "05_provenance_manifest.py",
    "06_generate_computational_chemistry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
