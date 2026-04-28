"""
Calculate hydrogen-like energy levels and transitions.

Run from article directory:
    python python/01_hydrogen_energy_levels.py
"""

from pathlib import Path

from electronic_structure_core import hydrogen_energy_levels, hydrogen_transitions_to_ground


ARTICLE_DIR = Path(__file__).resolve().parents[1]
LEVEL_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "hydrogen_energy_levels.csv"
TRANSITION_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "hydrogen_transitions.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "hydrogen_energy_levels_and_transitions.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    levels = hydrogen_energy_levels(max_n=6)
    transitions = hydrogen_transitions_to_ground(max_n=6)

    levels.to_csv(LEVEL_OUTPUT, index=False)
    transitions.to_csv(TRANSITION_OUTPUT, index=False)

    combined = levels.astype(str).assign(table_type="energy_levels")
    combined = combined._append(
        transitions.astype(str).assign(table_type="transitions"),
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Hydrogen energy levels")
    print(levels.round(6).to_string(index=False))
    print("\nTransitions to n=1")
    print(transitions.round(3).to_string(index=False))
    print(f"Saved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
