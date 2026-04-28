"""
Run all redox Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_cell_potential_gibbs.py",
    "02_nernst_equation.py",
    "03_redox_titration.py",
    "04_ph_corrosion_redox.py",
    "05_provenance_manifest.py",
    "06_generate_redox_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
