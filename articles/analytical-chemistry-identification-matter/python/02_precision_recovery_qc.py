"""
Calculate precision, spike recovery, and quality-control flags.

Run from article directory:
    python python/02_precision_recovery_qc.py
"""

from pathlib import Path
import pandas as pd

from analytical_core import replicate_precision, spike_recovery


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPLICATES_INPUT = ARTICLE_DIR / "data" / "replicate_measurements.csv"
SPIKES_INPUT = ARTICLE_DIR / "data" / "spike_recovery.csv"

PRECISION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "precision_summary.csv"
RECOVERY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "spike_recovery_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "precision_recovery_qc.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    precision = replicate_precision(pd.read_csv(REPLICATES_INPUT))
    recovery = spike_recovery(pd.read_csv(SPIKES_INPUT))

    precision["RSD_within_5_percent"] = (precision["RSD_percent"] <= 5.0).astype(int)

    precision.to_csv(PRECISION_OUTPUT, index=False)
    recovery.to_csv(RECOVERY_OUTPUT, index=False)

    combined = pd.concat(
        [
            precision.astype(str).assign(table_type="precision_summary"),
            recovery.astype(str).assign(table_type="spike_recovery_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Precision summary")
    print(precision.round(6).to_string(index=False))
    print("\nSpike recovery summary")
    print(recovery.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
