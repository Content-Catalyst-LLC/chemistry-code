"""
Calculate sequence composition and biomolecule class descriptors.

Run from article directory:
    python python/03_sequence_composition.py
"""

from pathlib import Path
import pandas as pd

from biochemistry_core import sequence_composition_table, biomolecule_class_descriptors


ARTICLE_DIR = Path(__file__).resolve().parents[1]
SEQ_INPUT = ARTICLE_DIR / "data" / "sequences.csv"
BIOMOL_INPUT = ARTICLE_DIR / "data" / "biomolecule_classes.csv"

SEQ_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "sequence_composition_only.csv"
BIOMOL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "biomolecule_class_descriptors.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "sequence_composition.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    sequence_result = sequence_composition_table(pd.read_csv(SEQ_INPUT))
    biomolecule_result = biomolecule_class_descriptors(pd.read_csv(BIOMOL_INPUT))

    sequence_result.to_csv(SEQ_OUTPUT, index=False)
    biomolecule_result.to_csv(BIOMOL_OUTPUT, index=False)

    combined = pd.concat(
        [
            sequence_result.astype(str).assign(table_type="sequence_composition"),
            biomolecule_result.astype(str).assign(table_type="biomolecule_class_descriptors"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Sequence composition")
    print(sequence_result.round(6).to_string(index=False))
    print("\nBiomolecule class descriptors")
    print(biomolecule_result.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
