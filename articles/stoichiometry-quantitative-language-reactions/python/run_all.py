"""
Run all stoichiometry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_limiting_reagent_yield.py",
    "02_solution_titration_gas.py",
    "03_empirical_formula_combustion.py",
    "04_reaction_extent_balances.py",
    "05_provenance_manifest.py",
    "06_generate_stoichiometry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
