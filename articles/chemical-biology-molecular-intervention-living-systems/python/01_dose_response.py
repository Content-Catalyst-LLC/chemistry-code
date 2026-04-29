"""
Calculate dose-response and target occupancy scaffolds.

Run from article directory:
    python python/01_dose_response.py
"""

from pathlib import Path
import pandas as pd

from chemical_biology_core import dose_response, occupancy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DOSE_INPUT = ARTICLE_DIR / "data" / "dose_response_cases.csv"
OCC_INPUT = ARTICLE_DIR / "data" / "occupancy_cases.csv"

DOSE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "dose_response_only.csv"
OCC_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "occupancy.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "dose_response.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    dose = dose_response(pd.read_csv(DOSE_INPUT))
    occ = occupancy(pd.read_csv(OCC_INPUT))

    dose.to_csv(DOSE_OUTPUT, index=False)
    occ.to_csv(OCC_OUTPUT, index=False)

    combined = pd.concat(
        [
            dose.astype(str).assign(table_type="dose_response"),
            occ.astype(str).assign(table_type="occupancy"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Dose response")
    print(dose.round(6).to_string(index=False))
    print("\nOccupancy")
    print(occ.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
