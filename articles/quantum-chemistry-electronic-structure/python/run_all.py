"""
Run all quantum chemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_orbital_mixing.py",
    "02_density_huckel.py",
    "03_basis_spin_states.py",
    "04_excited_states_tst.py",
    "05_provenance_manifest.py",
    "06_generate_quantum_chemistry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
