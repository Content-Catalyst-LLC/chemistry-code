"""
Build simplified molecular graph descriptors and adjacency matrices.

Run from article directory:
    python python/02_molecular_graphs.py
"""

from pathlib import Path
import pandas as pd

from organic_structure_core import molecular_graph_summary, adjacency_matrix_long


ARTICLE_DIR = Path(__file__).resolve().parents[1]
ATOMS_INPUT = ARTICLE_DIR / "data" / "molecular_graph_atoms.csv"
EDGES_INPUT = ARTICLE_DIR / "data" / "molecular_graph_edges.csv"
SUMMARY_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "molecular_graph_summary.csv"
ADJ_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "adjacency_matrix_long.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "molecular_graphs.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    atoms = pd.read_csv(ATOMS_INPUT)
    edges = pd.read_csv(EDGES_INPUT)

    summary = molecular_graph_summary(atoms, edges)
    adjacency = adjacency_matrix_long(atoms, edges)

    summary.to_csv(SUMMARY_OUTPUT, index=False)
    adjacency.to_csv(ADJ_OUTPUT, index=False)

    combined = pd.concat(
        [
            summary.astype(str).assign(table_type="molecular_graph_summary"),
            adjacency.astype(str).assign(table_type="adjacency_matrix_long"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Molecular graph summary")
    print(summary.round(6).to_string(index=False))
    print("\nAdjacency matrix long form")
    print(adjacency.head(30).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
