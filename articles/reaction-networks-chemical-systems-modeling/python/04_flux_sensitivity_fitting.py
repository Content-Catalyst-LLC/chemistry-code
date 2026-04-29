"""
Calculate flux table, sensitivity analysis, and simple parameter fitting.

Run from article directory:
    python python/04_flux_sensitivity_fitting.py
"""

from pathlib import Path
import pandas as pd

from reaction_network_core import (
    load_stoichiometric_matrix,
    flux_table_from_state,
    sensitivity_analysis,
    simple_fit_first_order_decay,
)


ARTICLE_DIR = Path(__file__).resolve().parents[1]
SENS_INPUT = ARTICLE_DIR / "data" / "sensitivity_cases.csv"
FIT_INPUT = ARTICLE_DIR / "data" / "fitting_data.csv"

FLUX_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "flux_table.csv"
SENS_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "sensitivity_analysis.csv"
FIT_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "simple_parameter_fit.csv"
COMBINED_OUTPUT = ARTICLE_DIR / "outputs" / "tables" / "flux_sensitivity_fitting.csv"


def main() -> None:
    COMBINED_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    _, _, stoich = load_stoichiometric_matrix(ARTICLE_DIR)

    flux = flux_table_from_state(
        concentration={"A": 0.60, "B": 0.30, "C": 0.05, "D": 0.03, "E": 0.02},
        parameters={"k1_A_to_B": 0.20, "k2_B_to_C": 0.08, "k3_A_to_D": 0.05, "k4_B_to_E": 0.03},
        stoich=stoich,
    )

    sensitivity = sensitivity_analysis(pd.read_csv(SENS_INPUT), stoich)
    fit = simple_fit_first_order_decay(pd.read_csv(FIT_INPUT))

    flux.to_csv(FLUX_OUTPUT, index=False)
    sensitivity.to_csv(SENS_OUTPUT, index=False)
    fit.to_csv(FIT_OUTPUT, index=False)

    combined = pd.concat(
        [
            flux.astype(str).assign(table_type="flux_table"),
            sensitivity.astype(str).assign(table_type="sensitivity_analysis"),
            fit.astype(str).assign(table_type="simple_parameter_fit"),
        ],
        ignore_index=True,
        sort=False,
    )
    combined.to_csv(COMBINED_OUTPUT, index=False)

    print("Flux table")
    print(flux.round(6).to_string(index=False))
    print("\nSensitivity analysis")
    print(sensitivity.round(6).to_string(index=False))
    print("\nSimple parameter fit")
    print(fit.round(6).to_string(index=False))
    print(f"\nSaved: {COMBINED_OUTPUT}")


if __name__ == "__main__":
    main()
