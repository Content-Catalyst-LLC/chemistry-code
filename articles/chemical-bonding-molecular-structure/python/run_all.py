"""
Run all chemical bonding Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_bond_geometry.py",
    "02_bond_polarity.py",
    "03_formal_charge_and_bond_order.py",
    "04_dipole_and_vsepr_summary.py",
    "05_provenance_manifest.py",
    "06_generate_bonding_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
