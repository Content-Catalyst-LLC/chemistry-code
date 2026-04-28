"""
Run all acid-base Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_weak_acid_base_ph.py",
    "02_buffer_henderson_hasselbalch.py",
    "03_titration_curves.py",
    "04_speciation_polyprotic.py",
    "05_provenance_manifest.py",
    "06_generate_acid_base_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
