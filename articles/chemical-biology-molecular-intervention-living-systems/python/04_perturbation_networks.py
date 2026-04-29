"""
Calculate perturbation-vector and network summaries.

Run from article directory:
    python python/04_perturbation_networks.py
"""

from pathlib import Path
import pandas as pd

from chemical_biology_core import perturbation_vector, network_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
PERTURB_INPUT = ARTICLE_DIR / "data" / "perturbation_features.csv"
NETWORK_INPUT = ARTICLE_DIR / "data" / "network_edges.csv"

PERTURB_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "perturbation_vector.csv"
NETWORK_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "network_summary.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "perturbation_networks.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    perturbation = perturbation_vector(pd.read_csv(PERTURB_INPUT))
    network = network_summary(pd.read_csv(NETWORK_INPUT))

    perturbation.to_csv(PERTURB_OUTPUT, index=False)
    network.to_csv(NETWORK_OUTPUT, index=False)

    combined = pd.concat(
        [
            perturbation.astype(str).assign(table_type="perturbation_vector"),
            network.astype(str).assign(table_type="network_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Perturbation vector")
    print(perturbation.round(6).to_string(index=False))
    print("\nNetwork summary")
    print(network.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
