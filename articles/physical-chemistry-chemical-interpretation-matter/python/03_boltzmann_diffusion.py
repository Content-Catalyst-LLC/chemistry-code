"""
Calculate Boltzmann populations and diffusion profiles.

Run from article directory:
    python python/03_boltzmann_diffusion.py
"""

from pathlib import Path
import pandas as pd

from physical_chemistry_core import boltzmann_populations, diffusion_profiles


ARTICLE_DIR = Path(__file__).resolve().parents[1]
BOLTZ_INPUT = ARTICLE_DIR / "data" / "boltzmann_states.csv"
DIFF_INPUT = ARTICLE_DIR / "data" / "diffusion_cases.csv"
BOLTZ_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "boltzmann_populations.csv"
DIFF_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "diffusion_profiles.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "boltzmann_diffusion.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    boltzmann = boltzmann_populations(pd.read_csv(BOLTZ_INPUT))
    diffusion = diffusion_profiles(pd.read_csv(DIFF_INPUT))

    boltzmann.to_csv(BOLTZ_OUTPUT, index=False)
    diffusion.to_csv(DIFF_OUTPUT, index=False)

    combined = pd.concat(
        [
            boltzmann.astype(str).assign(table_type="boltzmann_populations"),
            diffusion.astype(str).assign(table_type="diffusion_profiles"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Boltzmann populations")
    print(boltzmann.round(8).to_string(index=False))
    print("\nDiffusion profiles")
    print(diffusion.head(30).round(8).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
