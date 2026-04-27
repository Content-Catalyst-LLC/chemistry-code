"""
Calculate matrix eigenvalues and uncertainty summary.

Run from article directory:
    python python/04_linear_algebra_and_uncertainty.py
"""

from pathlib import Path
import pandas as pd

from math_chemistry_core import summarize_matrices, summarize_uncertainty


ARTICLE_DIR = Path(__file__).resolve().parents[1]
MATRIX_PATH = ARTICLE_DIR / "data" / "matrix_examples.csv"
UNCERTAINTY_PATH = ARTICLE_DIR / "data" / "uncertainty_components.csv"
MATRIX_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "matrix_eigenvalues.csv"
UNCERTAINTY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "uncertainty_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "linear_algebra_and_uncertainty.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    matrices = summarize_matrices(pd.read_csv(MATRIX_PATH))
    uncertainty = summarize_uncertainty(pd.read_csv(UNCERTAINTY_PATH), coverage_factor=2.0)

    matrices.to_csv(MATRIX_OUTPUT, index=False)
    uncertainty.to_csv(UNCERTAINTY_OUTPUT, index=False)

    combined = pd.concat(
        [
            matrices.astype(str).assign(table_type="linear_algebra"),
            uncertainty.astype(str).assign(table_type="uncertainty"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Matrix Eigenvalues")
    print(matrices.round(6).to_string(index=False))
    print("\nUncertainty")
    print(uncertainty.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
