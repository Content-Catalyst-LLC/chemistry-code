"""
Run all inorganic chemistry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_oxidation_states.py",
    "02_coordination_ligands.py",
    "03_crystal_field_magnetism.py",
    "04_ionic_materials_descriptors.py",
    "05_provenance_manifest.py",
    "06_generate_inorganic_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
