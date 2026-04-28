"""
Generate a report for Chemical Thermodynamics and Energetics.

Run from article directory:
    python python/06_generate_thermodynamics_report.py
"""

from pathlib import Path
import subprocess
import sys
import pandas as pd

from thermodynamics_core import dataframe_to_markdown


ARTICLE_DIR = Path(__file__).resolve().parents[1]
REPORT_PATH = ARTICLE_DIR / "outputs" / "reports" / "chemical_thermodynamics_report.md"

REQUIRED_OUTPUTS = [
    ("01_calorimetry_enthalpy.py", ARTICLE_DIR / "outputs" / "tables" / "calorimetry_enthalpy.csv"),
    ("02_hess_law_formation_enthalpy.py", ARTICLE_DIR / "outputs" / "tables" / "hess_law_formation_enthalpy.csv"),
    ("03_gibbs_equilibrium.py", ARTICLE_DIR / "outputs" / "tables" / "gibbs_equilibrium.csv"),
    ("04_vant_hoff_phase_coupling.py", ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_phase_coupling.csv"),
    ("05_provenance_manifest.py", ARTICLE_DIR / "outputs" / "manifests" / "provenance_manifest.csv"),
]


def ensure_outputs() -> None:
    for script, path in REQUIRED_OUTPUTS:
        if not path.exists():
            subprocess.run([sys.executable, str(ARTICLE_DIR / "python" / script)], check=True)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    ensure_outputs()

    calorimetry = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "calorimetry_enthalpy.csv").round(6)
    hess = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "hess_law_formation_enthalpy.csv").round(6)
    gibbs = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "gibbs_equilibrium.csv").round(6)
    vant = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "vant_hoff_fit.csv").round(6)
    phase = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "phase_transition_entropy.csv").round(6)
    coupled = pd.read_csv(ARTICLE_DIR / "outputs" / "tables" / "coupled_reactions.csv").round(6)

    report = [
        "# Chemical Thermodynamics and Energetics",
        "",
        "This report was generated from simplified educational thermodynamics data.",
        "",
        "## Calorimetry and Reaction Enthalpy",
        "",
        dataframe_to_markdown(calorimetry),
        "",
        "## Hess's Law Summary",
        "",
        dataframe_to_markdown(hess),
        "",
        "## Gibbs Free Energy and Equilibrium",
        "",
        dataframe_to_markdown(gibbs),
        "",
        "## van 't Hoff Fit",
        "",
        dataframe_to_markdown(vant),
        "",
        "## Phase Transition Entropy",
        "",
        dataframe_to_markdown(phase),
        "",
        "## Coupled Reactions",
        "",
        dataframe_to_markdown(coupled),
        "",
        "## Interpretation Warning",
        "",
        "These examples are educational scaffolds. Real thermodynamic work requires evaluated reference data, clear standard states, phase specification, uncertainty analysis, and expert judgment.",
        "",
    ]

    REPORT_PATH.write_text("\n".join(report))

    print("\n".join(report))
    print(f"Saved: {REPORT_PATH}")


if __name__ == "__main__":
    main()
