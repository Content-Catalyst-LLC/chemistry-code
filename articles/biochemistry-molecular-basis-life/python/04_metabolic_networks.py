"""
Calculate simplified metabolic flux balance, network summary, and biochemical free energy.

Run from article directory:
    python python/04_metabolic_networks.py
"""

from pathlib import Path
import pandas as pd

from biochemistry_core import flux_balance, network_summary, biochemical_free_energy


ARTICLE_DIR = Path(__file__).resolve().parents[1]
FLUX_INPUT = ARTICLE_DIR / "data" / "metabolic_flux_cases.csv"
STOICH_INPUT = ARTICLE_DIR / "data" / "stoichiometry.csv"
EDGES_INPUT = ARTICLE_DIR / "data" / "network_edges.csv"
ENERGY_INPUT = ARTICLE_DIR / "data" / "energy_cases.csv"

FLUX_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "flux_balance.csv"
NETWORK_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "network_summary.csv"
ENERGY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "biochemical_free_energy.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "metabolic_networks.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    flux_result = flux_balance(
        pd.read_csv(STOICH_INPUT),
        pd.read_csv(FLUX_INPUT),
    )
    network_result = network_summary(pd.read_csv(EDGES_INPUT))
    energy_result = biochemical_free_energy(pd.read_csv(ENERGY_INPUT))

    flux_result.to_csv(FLUX_OUTPUT, index=False)
    network_result.to_csv(NETWORK_OUTPUT, index=False)
    energy_result.to_csv(ENERGY_OUTPUT, index=False)

    combined = pd.concat(
        [
            flux_result.astype(str).assign(table_type="flux_balance"),
            network_result.astype(str).assign(table_type="network_summary"),
            energy_result.astype(str).assign(table_type="biochemical_free_energy"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Flux balance")
    print(flux_result.round(6).to_string(index=False))
    print("\nNetwork summary")
    print(network_result.to_string(index=False))
    print("\nBiochemical free energy")
    print(energy_result.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
