"""
Run all catalysis Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_barrier_rate_enhancement.py",
    "02_turnover_metrics.py",
    "03_adsorption_surface_rates.py",
    "04_catalytic_cycle_deactivation.py",
    "05_provenance_manifest.py",
    "06_generate_catalysis_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
