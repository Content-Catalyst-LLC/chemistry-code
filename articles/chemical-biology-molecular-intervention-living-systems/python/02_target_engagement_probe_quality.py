"""
Calculate target engagement and probe quality metrics.

Run from article directory:
    python python/02_target_engagement_probe_quality.py
"""

from pathlib import Path
import pandas as pd

from chemical_biology_core import target_engagement, probe_quality


ARTICLE_DIR = Path(__file__).resolve().parents[1]
TE_INPUT = ARTICLE_DIR / "data" / "target_engagement_cases.csv"
PROBE_INPUT = ARTICLE_DIR / "data" / "probe_quality_cases.csv"

TE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "target_engagement.csv"
PROBE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "probe_quality.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "target_engagement_probe_quality.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    te = target_engagement(pd.read_csv(TE_INPUT))
    probes = probe_quality(pd.read_csv(PROBE_INPUT))

    te.to_csv(TE_OUTPUT, index=False)
    probes.to_csv(PROBE_OUTPUT, index=False)

    combined = pd.concat(
        [
            te.astype(str).assign(table_type="target_engagement"),
            probes.astype(str).assign(table_type="probe_quality"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Target engagement")
    print(te.round(6).to_string(index=False))
    print("\nProbe quality")
    print(probes.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
