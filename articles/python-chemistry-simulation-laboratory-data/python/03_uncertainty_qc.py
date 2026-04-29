"""
Summarize replicate measurements and laboratory metadata.

Run from article directory:
    python python/03_uncertainty_qc.py
"""

from pathlib import Path
import pandas as pd

from python_chemistry_core import replicate_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPLICATES_INPUT = ARTICLE_DIR / "data" / "replicate_measurements.csv"
METADATA_INPUT = ARTICLE_DIR / "data" / "lab_metadata.csv"

REPLICATE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "replicate_summary.csv"
METADATA_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "lab_metadata_processed.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "uncertainty_qc.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    summary = replicate_summary(pd.read_csv(REPLICATES_INPUT))
    metadata = pd.read_csv(METADATA_INPUT)
    metadata["metadata_record_status"] = "recorded"

    summary.to_csv(REPLICATE_OUTPUT, index=False)
    metadata.to_csv(METADATA_OUTPUT, index=False)

    combined = pd.concat(
        [
            summary.astype(str).assign(table_type="replicate_summary"),
            metadata.astype(str).assign(table_type="lab_metadata"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Replicate summary")
    print(summary.round(6).to_string(index=False))
    print("\nLab metadata")
    print(metadata.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
