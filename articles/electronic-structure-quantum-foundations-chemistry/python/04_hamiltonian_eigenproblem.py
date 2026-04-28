"""
Calculate eigenvalues for small Hamiltonian-style matrices.

Run from article directory:
    python python/04_hamiltonian_eigenproblem.py
"""

from pathlib import Path
import pandas as pd

from electronic_structure_core import hamiltonian_eigenvalues


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "hamiltonian_matrices.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "hamiltonian_eigenvalues.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    matrices = pd.read_csv(INPUT_PATH)
    eigenvalues = hamiltonian_eigenvalues(matrices)
    eigenvalues.to_csv(OUTPUT_PATH, index=False)

    print(eigenvalues.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
