"""
Run all biochemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_enzyme_kinetics.py",
    "02_binding_occupancy.py",
    "03_sequence_composition.py",
    "04_metabolic_networks.py",
    "05_provenance_manifest.py",
    "06_generate_biochemistry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
