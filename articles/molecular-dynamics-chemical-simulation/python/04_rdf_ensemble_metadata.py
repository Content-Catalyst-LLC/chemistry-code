"""
Calculate RDF-like histogram and summarize ensemble metadata.

Run from article directory:
    python python/04_rdf_ensemble_metadata.py
"""

from pathlib import Path
import pandas as pd

from molecular_dynamics_core import rdf_histogram, ensemble_metadata, trajectory_summary


ARTICLE_DIR = Path(__file__).resolve().parents[1]
RDF_INPUT = ARTICLE_DIR / "data" / "rdf_distances.csv"
ENSEMBLE_INPUT = ARTICLE_DIR / "data" / "ensemble_protocols.csv"
SUMMARY_INPUT = ARTICLE_DIR / "data" / "trajectory_summary.csv"

RDF_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "rdf_histogram.csv"
ENSEMBLE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "ensemble_metadata.csv"
SUMMARY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "trajectory_summary_processed.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "rdf_ensemble_metadata.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    rdf = rdf_histogram(pd.read_csv(RDF_INPUT))
    ensemble = ensemble_metadata(pd.read_csv(ENSEMBLE_INPUT))
    summary = trajectory_summary(pd.read_csv(SUMMARY_INPUT))

    rdf.to_csv(RDF_OUTPUT, index=False)
    ensemble.to_csv(ENSEMBLE_OUTPUT, index=False)
    summary.to_csv(SUMMARY_OUTPUT, index=False)

    combined = pd.concat(
        [
            rdf.astype(str).assign(table_type="rdf_histogram"),
            ensemble.astype(str).assign(table_type="ensemble_metadata"),
            summary.astype(str).assign(table_type="trajectory_summary"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("RDF histogram")
    print(rdf.round(6).to_string(index=False))
    print("\nEnsemble metadata")
    print(ensemble.to_string(index=False))
    print("\nTrajectory summary")
    print(summary.to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
