"""
Run all electronic-structure Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_hydrogen_energy_levels.py",
    "02_orbital_capacity_and_configuration.py",
    "03_particle_in_box.py",
    "04_hamiltonian_eigenproblem.py",
    "05_provenance_manifest.py",
    "06_generate_electronic_structure_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
