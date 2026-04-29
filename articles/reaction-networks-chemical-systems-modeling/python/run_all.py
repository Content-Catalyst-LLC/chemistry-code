"""
Run all reaction-network Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_stoichiometric_matrix.py",
    "02_network_ode_simulation.py",
    "03_parallel_branching_selectivity.py",
    "04_flux_sensitivity_fitting.py",
    "05_provenance_manifest.py",
    "06_generate_network_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
