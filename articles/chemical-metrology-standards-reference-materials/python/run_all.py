"""
Run all chemical metrology Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_uncertainty_budget.py",
    "02_reference_material_summary.py",
    "03_traceability_chain.py",
    "04_interlaboratory_comparison.py",
    "05_provenance_manifest.py",
    "06_generate_metrology_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
