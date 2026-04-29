"""
Replicate summary scaffold for chemistry statistics.

Run from article directory:
    python python/replicate_summary.py
"""

from pathlib import Path
import pandas as pd


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "replicate_measurements.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "python_replicate_summary.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    summary = (
        data.groupby(["sample_id", "analyte", "method_id", "batch_id"], as_index=False)
        .agg(
            mean_mM=("measurement_mM", "mean"),
            sd_mM=("measurement_mM", "std"),
            n=("measurement_mM", "count"),
        )
    )
    summary["se_mM"] = summary["sd_mM"] / summary["n"] ** 0.5
    summary["rsd_percent"] = 100 * summary["sd_mM"] / summary["mean_mM"]

    summary.to_csv(OUTPUT_PATH, index=False)
    print(summary.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
