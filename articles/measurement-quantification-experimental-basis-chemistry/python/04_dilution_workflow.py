"""
Calculate dilution plans using C1V1 = C2V2.

Run from article directory:
    python python/04_dilution_workflow.py
"""

from pathlib import Path
import pandas as pd

from measurement_quantification_core import calculate_dilution_plan


ARTICLE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = ARTICLE_DIR / "data" / "dilution_plan.csv"
OUTPUT_PATH = ARTICLE_DIR / "outputs" / "tables" / "dilution_plan_calculated.csv"


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(INPUT_PATH)
    result = calculate_dilution_plan(data)

    result.to_csv(OUTPUT_PATH, index=False)

    print(result.round(6).to_string(index=False))
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
