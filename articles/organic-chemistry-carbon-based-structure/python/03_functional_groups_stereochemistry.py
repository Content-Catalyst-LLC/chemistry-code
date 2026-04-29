"""
Summarize functional group flags and stereochemistry scaffolds.

Run from article directory:
    python python/03_functional_groups_stereochemistry.py
"""

from pathlib import Path
import pandas as pd

from organic_structure_core import functional_group_summary, stereochemistry_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
GROUP_INPUT = ARTICLE_DIR / "data" / "functional_group_cases.csv"
STEREO_INPUT = ARTICLE_DIR / "data" / "stereochemistry_cases.csv"
GROUP_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "functional_group_summary.csv"
STEREO_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "stereochemistry_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "functional_groups_stereochemistry.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    groups = functional_group_summary(pd.read_csv(GROUP_INPUT))
    stereo = stereochemistry_summary(pd.read_csv(STEREO_INPUT))

    groups.to_csv(GROUP_OUTPUT, index=False)
    stereo.to_csv(STEREO_OUTPUT, index=False)

    combined = pd.concat(
        [
            groups.astype(str).assign(table_type="functional_group_summary"),
            stereo.astype(str).assign(table_type="stereochemistry_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Functional group summary")
    print(groups.to_string(index=False))
    print("\nStereochemistry summary")
    print(stereo.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
