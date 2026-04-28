"""
Summarize phase-property and surface-tension tables.

Run from article directory:
    python python/04_phase_property_summary.py
"""

from pathlib import Path
import pandas as pd

from condensed_matter_core import summarize_phase_properties


ARTICLE_DIR = Path(__file__).resolve().parents[1]
PHASE_INPUT = ARTICLE_DIR / "data" / "phase_properties_sample.csv"
SURFACE_INPUT = ARTICLE_DIR / "data" / "surface_tension_sample.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "phase_property_summary.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    phase = pd.read_csv(PHASE_INPUT)
    surface = pd.read_csv(SURFACE_INPUT)

    summaries = summarize_phase_properties(phase, surface)

    combined = pd.concat(
        [
            table.assign(summary_type=name).astype(str)
            for name, table in summaries.items()
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(OUTPUT_PATH, index=False)

    for name, table in summaries.items():
        print(f"\n{name}")
        print(table.round(4).to_string(index=False))

    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
