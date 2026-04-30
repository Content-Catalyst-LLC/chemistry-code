#!/usr/bin/env python3
"""
Advanced astrochemistry workflow for the article:
Astrochemistry and the Molecular Universe

This module provides educational, reproducible scaffolding for:

1. Doppler-corrected spectral-line matching
2. Synthetic Gaussian spectral profiles
3. Rotational-diagram temperature estimation
4. Fractional abundance screening
5. Thermal desorption modeling
6. Photodissociation lifetime modeling
7. Simplified astrochemical reaction-network integration

All data are synthetic. This is not professional radiative transfer,
line identification, exoplanet retrieval, or biosignature analysis.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


C_KM_S = 299_792.458
PLANCK_J_S = 6.62607015e-34
BOLTZMANN_J_K = 1.380649e-23
SECONDS_PER_YEAR = 365.25 * 24 * 3600


ARTICLE_DIR = Path(__file__).resolve().parents[2]
ADV_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ADV_DIR / "data"
OUT_TABLES = ADV_DIR / "outputs" / "tables"
OUT_REPORTS = ADV_DIR / "outputs" / "reports"
OUT_MANIFESTS = ADV_DIR / "outputs" / "manifests"


@dataclass
class CatalogLine:
    species: str
    transition: str
    rest_frequency_GHz: float
    upper_energy_K: float
    einstein_A_s1: float
    g_upper: float
    molecule_class: str


@dataclass
class ObservedLine:
    source: str
    environment: str
    observed_frequency_GHz: float
    peak_intensity_K: float
    line_width_km_s: float
    integrated_intensity_K_km_s: float
    noise_K: float


@dataclass
class LineMatch:
    source: str
    environment: str
    species: str
    transition: str
    rest_frequency_GHz: float
    observed_frequency_GHz: float
    frequency_offset_MHz: float
    radial_velocity_km_s: float
    signal_to_noise: float
    match_quality: str


def load_catalog(path: Path) -> list[CatalogLine]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            CatalogLine(
                species=row["species"],
                transition=row["transition"],
                rest_frequency_GHz=float(row["rest_frequency_GHz"]),
                upper_energy_K=float(row["upper_energy_K"]),
                einstein_A_s1=float(row["einstein_A_s1"]),
                g_upper=float(row["g_upper"]),
                molecule_class=row["molecule_class"],
            )
            for row in reader
        ]


def load_observations(path: Path) -> list[ObservedLine]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [
            ObservedLine(
                source=row["source"],
                environment=row["environment"],
                observed_frequency_GHz=float(row["observed_frequency_GHz"]),
                peak_intensity_K=float(row["peak_intensity_K"]),
                line_width_km_s=float(row["line_width_km_s"]),
                integrated_intensity_K_km_s=float(row["integrated_intensity_K_km_s"]),
                noise_K=float(row["noise_K"]),
            )
            for row in reader
        ]


def radial_velocity_km_s(rest_frequency_GHz: float, observed_frequency_GHz: float) -> float:
    """
    Nonrelativistic Doppler velocity:

    Δν / ν0 ≈ -v / c

    Positive velocity here corresponds to redshifted observed frequency.
    """
    return -C_KM_S * (observed_frequency_GHz - rest_frequency_GHz) / rest_frequency_GHz


def photon_energy_J(frequency_GHz: float) -> float:
    """Photon energy E = hν."""
    return PLANCK_J_S * frequency_GHz * 1e9


def match_lines(
    catalog: Iterable[CatalogLine],
    observations: Iterable[ObservedLine],
    tolerance_MHz: float = 8.0,
) -> list[LineMatch]:
    """
    Match observed lines to catalog lines within a frequency tolerance.

    This is a first-pass matching screen, not a professional molecular detection.
    """
    matches: list[LineMatch] = []

    for obs in observations:
        for line in catalog:
            offset_MHz = (obs.observed_frequency_GHz - line.rest_frequency_GHz) * 1000.0
            if abs(offset_MHz) <= tolerance_MHz:
                velocity = radial_velocity_km_s(line.rest_frequency_GHz, obs.observed_frequency_GHz)
                snr = obs.peak_intensity_K / obs.noise_K if obs.noise_K > 0 else float("inf")

                if snr >= 10 and abs(velocity) <= 30:
                    quality = "strong_screen"
                elif snr >= 5 and abs(velocity) <= 50:
                    quality = "moderate_screen"
                else:
                    quality = "weak_or_check_screen"

                matches.append(
                    LineMatch(
                        source=obs.source,
                        environment=obs.environment,
                        species=line.species,
                        transition=line.transition,
                        rest_frequency_GHz=line.rest_frequency_GHz,
                        observed_frequency_GHz=obs.observed_frequency_GHz,
                        frequency_offset_MHz=offset_MHz,
                        radial_velocity_km_s=velocity,
                        signal_to_noise=snr,
                        match_quality=quality,
                    )
                )

    return matches


def gaussian_line_profile(
    center_GHz: float,
    peak_K: float,
    fwhm_km_s: float,
    rest_frequency_GHz: float,
    span_MHz: float = 30.0,
    n_points: int = 301,
) -> list[dict]:
    """
    Generate a synthetic Gaussian spectral line.

    The width is converted from km/s to GHz using Δν/ν ≈ v/c.
    """
    fwhm_GHz = rest_frequency_GHz * (fwhm_km_s / C_KM_S)
    sigma_GHz = fwhm_GHz / (2.0 * math.sqrt(2.0 * math.log(2.0)))

    start = center_GHz - span_MHz / 2000.0
    step = (span_MHz / 1000.0) / (n_points - 1)

    rows = []
    for i in range(n_points):
        frequency = start + i * step
        intensity = peak_K * math.exp(-0.5 * ((frequency - center_GHz) / sigma_GHz) ** 2)
        rows.append(
            {
                "frequency_GHz": frequency,
                "intensity_K": intensity,
                "center_GHz": center_GHz,
                "fwhm_km_s": fwhm_km_s,
            }
        )

    return rows


def rotational_diagram_temperature(
    transitions: list[dict],
) -> dict:
    """
    Estimate a rotational temperature from a simple rotational diagram.

    For optically thin LTE emission, a simplified relation is:

    ln(N_u / g_u) = intercept - E_u / T_rot

    This synthetic implementation uses integrated intensity as a proxy for N_u.
    It is not a research-grade column-density calculation.
    """
    if len(transitions) < 2:
        raise ValueError("At least two transitions are required.")

    x_values = []
    y_values = []

    for row in transitions:
        intensity = float(row["integrated_intensity_K_km_s"])
        g_upper = float(row["g_upper"])
        upper_energy_K = float(row["upper_energy_K"])

        if intensity <= 0 or g_upper <= 0:
            continue

        x_values.append(upper_energy_K)
        y_values.append(math.log(intensity / g_upper))

    n = len(x_values)
    if n < 2:
        raise ValueError("Insufficient valid transition intensities.")

    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    denominator = sum((x - mean_x) ** 2 for x in x_values)

    slope = numerator / denominator
    intercept = mean_y - slope * mean_x

    # slope = -1 / T_rot
    rotational_temperature_K = -1.0 / slope if slope != 0 else float("inf")

    fitted = []
    for x, y in zip(x_values, y_values):
        y_hat = intercept + slope * x
        fitted.append(
            {
                "upper_energy_K": x,
                "ln_intensity_over_g": y,
                "fitted_ln_intensity_over_g": y_hat,
                "residual": y - y_hat,
            }
        )

    return {
        "rotational_temperature_K": rotational_temperature_K,
        "slope": slope,
        "intercept": intercept,
        "n_transitions": n,
        "fitted_points": fitted,
    }


def fractional_abundance(column_density_cm2: float, h2_column_density_cm2: float) -> float:
    """Fractional abundance relative to H2 column density."""
    return column_density_cm2 / h2_column_density_cm2


def thermal_desorption_rate_s1(
    binding_energy_K: float,
    dust_temperature_K: float,
    attempt_frequency_s1: float = 1e12,
) -> float:
    """
    Simplified thermal desorption rate.

    k_des = ν0 exp(-E_b / T)
    """
    return attempt_frequency_s1 * math.exp(-binding_energy_K / dust_temperature_K)


def photodissociation_lifetime_years(
    uv_field_index: float,
    base_rate_s1: float = 1e-10,
    shielding_factor: float = 1.0,
) -> float:
    """
    Simplified photodissociation lifetime.

    k_ph = base_rate * UV * shielding_factor
    """
    k_ph = base_rate_s1 * max(uv_field_index, 1e-12) * shielding_factor
    return 1.0 / k_ph / SECONDS_PER_YEAR


def integrate_reaction_network(
    t_end_years: float = 1e5,
    dt_years: float = 1e3,
) -> list[dict]:
    """
    Integrate a toy astrochemical reaction network.

    Species:
    - CO
    - H3+
    - HCO+
    - e-

    Reactions:
    1. H3+ + CO -> HCO+ + H2
    2. HCO+ + e- -> CO + H

    This is a toy pedagogical model using explicit Euler integration.
    """
    seconds_per_year = SECONDS_PER_YEAR
    dt_s = dt_years * seconds_per_year
    steps = int(t_end_years / dt_years)

    # Number densities in cm^-3, synthetic.
    co = 1.0e-4
    h3p = 1.0e-8
    hcop = 1.0e-10
    electron = 1.0e-7

    # Rate coefficients in cm^3 s^-1, illustrative.
    k_form = 1.7e-9
    k_recomb = 2.0e-7

    rows = []

    for step in range(steps + 1):
        t_years = step * dt_years

        rows.append(
            {
                "time_years": t_years,
                "CO_fraction": co,
                "H3plus_fraction": h3p,
                "HCOplus_fraction": hcop,
                "electron_fraction": electron,
            }
        )

        formation = k_form * h3p * co
        recombination = k_recomb * hcop * electron

        d_co = (-formation + recombination) * dt_s
        d_h3p = (-formation) * dt_s
        d_hcop = (formation - recombination) * dt_s

        co = max(co + d_co, 0.0)
        h3p = max(h3p + d_h3p, 0.0)
        hcop = max(hcop + d_hcop, 0.0)

    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)
    OUT_REPORTS.mkdir(parents=True, exist_ok=True)
    OUT_MANIFESTS.mkdir(parents=True, exist_ok=True)

    catalog = load_catalog(DATA_DIR / "line_catalog_synthetic.csv")
    observations = load_observations(DATA_DIR / "observed_lines_synthetic.csv")

    matches = match_lines(catalog, observations, tolerance_MHz=8.0)
    match_rows = [asdict(match) for match in matches]
    write_csv(OUT_TABLES / "advanced_line_matches.csv", match_rows)

    # Generate a synthetic spectrum around the first CO observation.
    spectrum = gaussian_line_profile(
        center_GHz=115.269,
        peak_K=4.2,
        fwhm_km_s=1.4,
        rest_frequency_GHz=115.271,
    )
    write_csv(OUT_TABLES / "synthetic_gaussian_spectrum.csv", spectrum)

    # Rotational diagram using synthetic CH3OH matched transitions.
    ch3oh_catalog = {line.transition: line for line in catalog if line.species == "CH3OH"}
    ch3oh_obs = [
        obs for obs in observations
        if abs(obs.observed_frequency_GHz - 96.738) < 0.01
        or abs(obs.observed_frequency_GHz - 145.099) < 0.01
        or abs(obs.observed_frequency_GHz - 193.448) < 0.01
    ]

    rotational_rows = []
    for obs in ch3oh_obs:
        nearest = min(
            ch3oh_catalog.values(),
            key=lambda line: abs(line.rest_frequency_GHz - obs.observed_frequency_GHz),
        )
        rotational_rows.append(
            {
                "transition": nearest.transition,
                "upper_energy_K": nearest.upper_energy_K,
                "g_upper": nearest.g_upper,
                "integrated_intensity_K_km_s": obs.integrated_intensity_K_km_s,
            }
        )

    rot = rotational_diagram_temperature(rotational_rows)
    write_csv(OUT_TABLES / "rotational_diagram_points.csv", rot["fitted_points"])

    reaction_rows = integrate_reaction_network()
    write_csv(OUT_TABLES / "toy_reaction_network_timeseries.csv", reaction_rows)

    # Desorption and photochemistry screens.
    chemistry_rows = []
    for species, binding_energy, temp, uv in [
        ("CO", 855.0, 10.0, 0.2),
        ("CH3OH", 5500.0, 120.0, 8.0),
        ("H2O", 5700.0, 160.0, 12.0),
        ("CO2", 2575.0, 900.0, 150.0),
    ]:
        chemistry_rows.append(
            {
                "species": species,
                "binding_energy_K": binding_energy,
                "dust_temperature_K": temp,
                "uv_field_index": uv,
                "desorption_rate_s1": thermal_desorption_rate_s1(binding_energy, temp),
                "photodissociation_lifetime_years": photodissociation_lifetime_years(uv),
            }
        )

    write_csv(OUT_TABLES / "desorption_photochemistry_screen.csv", chemistry_rows)

    report = [
        "# Advanced Astrochemistry Computational Report",
        "",
        f"Line matches generated: {len(match_rows)}",
        f"Rotational temperature estimate for synthetic CH3OH set: {rot['rotational_temperature_K']:.2f} K",
        f"Reaction-network time steps: {len(reaction_rows)}",
        "",
        "## Notes",
        "",
        "- All values are synthetic and educational.",
        "- Line matching is frequency-based only and does not constitute molecular identification.",
        "- Rotational-diagram analysis uses integrated intensity as a proxy and omits optical-depth and partition-function corrections.",
        "- Reaction-network integration is a toy model, not a validated astrochemical network.",
    ]

    (OUT_REPORTS / "advanced_astrochemistry_report.md").write_text(
        "\n".join(report),
        encoding="utf-8",
    )

    manifest = {
        "article_slug": "astrochemistry-molecular-universe",
        "advanced_layer": True,
        "outputs": [
            "advanced/outputs/tables/advanced_line_matches.csv",
            "advanced/outputs/tables/synthetic_gaussian_spectrum.csv",
            "advanced/outputs/tables/rotational_diagram_points.csv",
            "advanced/outputs/tables/toy_reaction_network_timeseries.csv",
            "advanced/outputs/tables/desorption_photochemistry_screen.csv",
            "advanced/outputs/reports/advanced_astrochemistry_report.md",
        ],
        "responsible_use": "Educational synthetic astrochemistry code only; not professional line identification, radiative transfer, exoplanet retrieval, or biosignature assessment.",
    }

    (OUT_MANIFESTS / "advanced_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("Advanced astrochemistry workflow complete.")
    print(f"Line matches: {len(match_rows)}")
    print(f"Synthetic CH3OH rotational temperature: {rot['rotational_temperature_K']:.2f} K")
    print(f"Outputs written to: {ADV_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
