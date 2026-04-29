"""
Calculate Lennard-Jones potentials and Tanimoto similarities.

Run from article directory:
    python python/03_potentials_similarity.py
"""

from pathlib import Path
import pandas as pd

from computational_chemistry_core import lennard_jones, tanimoto_similarity_from_fingerprints


ARTICLE_DIR = Path(__file__).resolve().parents[1]
LJ_INPUT = ARTICLE_DIR / "data" / "lennard_jones_cases.csv"
FP_INPUT = ARTICLE_DIR / "data" / "fingerprints.csv"

LJ_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "lennard_jones.csv"
FP_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "tanimoto_similarity.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "potentials_similarity.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    lj = lennard_jones(pd.read_csv(LJ_INPUT))
    fp = tanimoto_similarity_from_fingerprints(pd.read_csv(FP_INPUT))

    lj.to_csv(LJ_OUTPUT, index=False)
    fp.to_csv(FP_OUTPUT, index=False)

    combined = pd.concat(
        [
            lj.astype(str).assign(table_type="lennard_jones"),
            fp.astype(str).assign(table_type="tanimoto_similarity"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Lennard-Jones")
    print(lj.round(6).to_string(index=False))
    print("\nTanimoto similarity")
    print(fp.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
