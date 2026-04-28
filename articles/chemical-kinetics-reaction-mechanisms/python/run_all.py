"""
Run all chemical kinetics Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_integrated_rate_laws.py",
    "02_arrhenius_analysis.py",
    "03_reaction_mechanism_odes.py",
    "04_enzyme_kinetics.py",
    "05_provenance_manifest.py",
    "06_generate_kinetics_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
