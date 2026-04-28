"""
Run all chemical equilibrium Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_reaction_quotient_free_energy.py",
    "02_equilibrium_solver.py",
    "03_reversible_dynamics.py",
    "04_vant_hoff_solubility_activity.py",
    "05_provenance_manifest.py",
    "06_generate_equilibrium_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
