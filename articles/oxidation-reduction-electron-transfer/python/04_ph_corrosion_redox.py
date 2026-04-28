"""
Generate pH-dependent redox potential and corrosion-pair scaffolds.

Run from article directory:
    python python/04_ph_corrosion_redox.py
"""

from pathlib import Path
import pandas as pd

from redox_core import ph_dependent_redox, corrosion_pair_analysis


ARTICLE_DIR = Path(__file__).resolve().parents[1]

PH_INPUT = ARTICLE_DIR / "data" / "ph_redox_cases.csv"
CORROSION_INPUT = ARTICLE_DIR / "data" / "corrosion_pairs.csv"

PH_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "ph_dependent_redox.csv"
CORROSION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "corrosion_pairs.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "ph_corrosion_redox.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    ph_profile = ph_dependent_redox(pd.read_csv(PH_INPUT))
    corrosion = corrosion_pair_analysis(pd.read_csv(CORROSION_INPUT))

    ph_profile.to_csv(PH_OUTPUT, index=False)
    corrosion.to_csv(CORROSION_OUTPUT, index=False)

    combined = pd.concat(
        [
            ph_profile.astype(str).assign(table_type="ph_dependent_redox"),
            corrosion.astype(str).assign(table_type="corrosion_pair_analysis"),
        ],
        ignore_index=True,
        sort=False,
    )

    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("pH-dependent redox")
    print(ph_profile.head(20).round(6).to_string(index=False))
    print("\nCorrosion pair scaffold")
    print(corrosion.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
