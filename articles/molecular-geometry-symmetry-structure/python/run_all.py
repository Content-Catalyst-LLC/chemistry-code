"""
Run all molecular geometry Python workflows.

Run from article directory:
    python python/run_all.py
"""

from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "01_distance_matrix_and_angles.py",
    "02_centers_and_extents.py",
    "03_rotation_and_symmetry_operation.py",
    "04_conformer_rmsd_and_torsion.py",
    "05_provenance_manifest.py",
    "06_generate_geometry_report.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"\n=== Running {script} ===")
        subprocess.run([sys.executable, str(SCRIPT_DIR / script)], check=True)


if __name__ == "__main__":
    main()
