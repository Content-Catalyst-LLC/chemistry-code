"""
Calculate Langmuir adsorption, surface rates, and Michaelis-Menten rates.

Run from article directory:
    python python/03_adsorption_surface_rates.py
"""

from pathlib import Path
import pandas as pd

from catalysis_core import adsorption_surface_rates, michaelis_menten_rates


ARTICLE_DIR = Path(__file__).resolve().parents[1]
ADS_INPUT = ARTICLE_DIR / "data" / "adsorption_cases.csv"
ENZYME_INPUT = ARTICLE_DIR / "data" / "enzyme_cases.csv"
ADS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "adsorption_surface_rates_only.csv"
ENZYME_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "michaelis_menten_rates.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "adsorption_surface_rates.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    adsorption = adsorption_surface_rates(pd.read_csv(ADS_INPUT))
    enzyme = michaelis_menten_rates(pd.read_csv(ENZYME_INPUT))

    adsorption.to_csv(ADS_OUTPUT, index=False)
    enzyme.to_csv(ENZYME_OUTPUT, index=False)

    combined = pd.concat(
        [
            adsorption.astype(str).assign(table_type="langmuir_surface_rate"),
            enzyme.astype(str).assign(table_type="michaelis_menten"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Langmuir surface rates")
    print(adsorption.round(6).to_string(index=False))
    print("\nMichaelis-Menten rates")
    print(enzyme.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
