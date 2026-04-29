"""
Run all organic-structure Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_formula_descriptors.py",
    "02_molecular_graphs.py",
    "03_functional_groups_stereochemistry.py",
    "04_structure_property_scaffold.py",
    "05_provenance_manifest.py",
    "06_generate_organic_structure_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
