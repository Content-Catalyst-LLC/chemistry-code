"""
Fit van 't Hoff data, summarize phase transitions, and sum coupled reactions.

Run from article directory:
    python python/04_vant_hoff_phase_coupling.py
"""

from pathlib import Path
import pandas as pd

from thermodynamics_core import vant_hoff_fit, phase_transition_entropy, coupled_reactions


ARTICLE_DIR = Path(__file__).resolve().parents[1]
VANT_INPUT = ARTICLE_DIR / "data" / "vant_hoff_examples.csv"
PHASE_INPUT = ARTICLE_DIR / "data" / "phase_transition_examples.csv"
COUPLED_INPUT = ARTICLE_DIR / "data" / "coupled_reaction_examples.csv"

VANT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_fit.csv"
PHASE_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "phase_transition_entropy.csv"
COUPLED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "coupled_reactions.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_phase_coupling.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    vant = vant_hoff_fit(pd.read_csv(VANT_INPUT))
    phase = phase_transition_entropy(pd.read_csv(PHASE_INPUT))
    coupled = coupled_reactions(pd.read_csv(COUPLED_INPUT))

    vant.to_csv(VANT_OUTPUT, index=False)
    phase.to_csv(PHASE_OUTPUT, index=False)
    coupled.to_csv(COUPLED_OUTPUT, index=False)

    combined = pd.concat(
        [
            vant.astype(str).assign(table_type="vant_hoff_fit"),
            phase.astype(str).assign(table_type="phase_transition_entropy"),
            coupled.astype(str).assign(table_type="coupled_reactions"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("van 't Hoff fit")
    print(vant.round(6).to_string(index=False))
    print("\nPhase transitions")
    print(phase.round(6).to_string(index=False))
    print("\nCoupled reactions")
    print(coupled.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
