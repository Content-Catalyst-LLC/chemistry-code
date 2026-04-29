"""
Calculate calibration model, unknown concentrations, LOD, and LOQ.

Run from article directory:
    python python/01_calibration_lod_loq.py
"""

from pathlib import Path
import pandas as pd

from analytical_core import calibration_lod_loq


ARTICLE_DIR = Path(__file__).resolve().parents[1]
STANDARDS_INPUT = ARTICLE_DIR / "data" / "calibration_standards.csv"
BLANKS_INPUT = ARTICLE_DIR / "data" / "blank_signals.csv"
UNKNOWNS_INPUT = ARTICLE_DIR / "data" / "unknown_samples.csv"

MODEL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "calibration_model.csv"
UNKNOWNS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "unknown_concentrations.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "calibration_lod_loq.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    standards = pd.read_csv(STANDARDS_INPUT)
    blanks = pd.read_csv(BLANKS_INPUT)
    unknowns = pd.read_csv(UNKNOWNS_INPUT)

    model_table, concentration_table = calibration_lod_loq(standards, blanks, unknowns)

    model_table.to_csv(MODEL_OUTPUT, index=False)
    concentration_table.to_csv(UNKNOWNS_OUTPUT, index=False)

    combined = pd.concat(
        [
            model_table.astype(str).assign(table_type="calibration_model"),
            concentration_table.astype(str).assign(table_type="unknown_concentrations"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Calibration model")
    print(model_table.round(8).to_string(index=False))
    print("\nUnknown concentrations")
    print(concentration_table.round(8).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
