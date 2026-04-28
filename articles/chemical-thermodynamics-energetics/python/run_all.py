"""
Run all chemical thermodynamics Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_calorimetry_enthalpy.py",
    "02_hess_law_formation_enthalpy.py",
    "03_gibbs_equilibrium.py",
    "04_vant_hoff_phase_coupling.py",
    "05_provenance_manifest.py",
    "06_generate_thermodynamics_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
