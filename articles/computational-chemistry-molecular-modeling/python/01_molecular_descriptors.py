"""
Calculate molecular descriptor and molecular graph scaffolds.

Run from article directory:
    python python/01_molecular_descriptors.py
"""

from pathlib import Path
import pandas as pd

from computational_chemistry_core import descriptor_table, graph_table


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DESC_INPUT = ARTICLE_DIR / "data" / "molecular_descriptors.csv"
GRAPH_INPUT = ARTICLE_DIR / "data" / "molecular_graphs.csv"

DESC_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "descriptor_table.csv"
GRAPH_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "graph_table.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "molecular_descriptors.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    descriptors = descriptor_table(pd.read_csv(DESC_INPUT))
    graphs = graph_table(pd.read_csv(GRAPH_INPUT))

    descriptors.to_csv(DESC_OUTPUT, index=False)
    graphs.to_csv(GRAPH_OUTPUT, index=False)

    combined = pd.concat(
        [
            descriptors.astype(str).assign(table_type="descriptor_table"),
            graphs.astype(str).assign(table_type="graph_table"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Descriptor table")
    print(descriptors.round(6).to_string(index=False))
    print("\nGraph table")
    print(graphs.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
