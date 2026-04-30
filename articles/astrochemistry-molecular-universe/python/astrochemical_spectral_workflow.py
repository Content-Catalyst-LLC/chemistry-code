#!/usr/bin/env python3
"""
Astrochemistry workflow:
- Load synthetic astrochemical line-survey data.
- Estimate radial velocity from observed and rest frequencies.
- Estimate fractional abundance relative to H2.
- Screen simplified thermal desorption and photochemical processing.
- Write output tables, report, and provenance manifest.

Educational only. Not for professional molecular line identification,
radiative-transfer modeling, mission analysis, or biosignature assessment.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean


ARTICLE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = ARTICLE_DIR / "data" / "astrochemical_survey_synthetic.csv"
TABLE_DIR = ARTICLE_DIR / "outputs" / "tables"
REPORT_DIR = ARTICLE_DIR / "outputs" / "reports"
MANIFEST_DIR = ARTICLE_DIR / "outputs" / "manifests"

C_KM_S = 299792.458
PLANCK_J_S = 6.62607015e-34

NUMERIC_FIELDS = [
    "rest_frequency_GHz",
    "observed_frequency_GHz",
    "integrated_intensity_K_km_s",
    "column_density_cm2",
    "H2_column_density_cm2",
    "dust_temperature_K",
    "gas_temperature_K",
    "uv_field_index",
    "cosmic_ray_ionization_rate_s1",
    "binding_energy_K",
]


def parse_float(value: str) -> float | None:
    value = value.strip()
    if value == "" or value.upper() == "NA":
        return None
    return float(value)


def load_rows() -> list[dict]:
    rows = []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            for field in NUMERIC_FIELDS:
                row[field] = parse_float(row[field])
            rows.append(row)
    return rows


def radial_velocity_km_s(rest_frequency_ghz: float, observed_frequency_ghz: float) -> float:
    """
    Nonrelativistic Doppler velocity estimate.

    delta_nu / nu0 ≈ -v/c
    """
    return -C_KM_S * (observed_frequency_ghz - rest_frequency_ghz) / rest_frequency_ghz


def photon_energy_j(frequency_ghz: float) -> float:
    """Photon energy E = h nu."""
    return PLANCK_J_S * frequency_ghz * 1.0e9


def fractional_abundance(column_density: float, h2_column_density: float) -> float:
    """Fractional abundance relative to molecular hydrogen."""
    return column_density / h2_column_density


def desorption_rate_s1(binding_energy_k: float, dust_temperature_k: float, attempt_frequency_s1: float = 1.0e12) -> float:
    """
    Simplified thermal desorption rate.

    k_des = nu0 * exp(-E_b / T)

    Binding energy is represented in kelvin for this teaching example.
    """
    return attempt_frequency_s1 * math.exp(-binding_energy_k / dust_temperature_k)


def photodissociation_lifetime_years(uv_field_index: float, base_rate_s1: float = 1.0e-10) -> float:
    """
    Simplified photodissociation lifetime.

    k_ph = base_rate * UV_index
    """
    k_ph = base_rate_s1 * max(uv_field_index, 1.0e-12)
    seconds_per_year = 365.25 * 24 * 3600
    return 1.0 / k_ph / seconds_per_year


def add_indicators(rows: list[dict]) -> list[dict]:
    enriched = []

    for row in rows:
        item = dict(row)
        item["radial_velocity_km_s"] = radial_velocity_km_s(
            row["rest_frequency_GHz"],
            row["observed_frequency_GHz"],
        )
        item["photon_energy_J"] = photon_energy_j(row["rest_frequency_GHz"])
        item["fractional_abundance"] = fractional_abundance(
            row["column_density_cm2"],
            row["H2_column_density_cm2"],
        )
        item["desorption_rate_s1_simplified"] = desorption_rate_s1(
            row["binding_energy_K"],
            row["dust_temperature_K"],
        )
        item["photodissociation_lifetime_years_simplified"] = photodissociation_lifetime_years(
            row["uv_field_index"],
        )
        item["thermal_release_screen"] = (
            "thermal_release_attention"
            if item["desorption_rate_s1_simplified"] > 1.0e-6
            else "ice_retention_or_slow_release_screen"
        )
        item["photochemical_screen"] = (
            "high_photochemical_processing"
            if row["uv_field_index"] > 10
            else "lower_photochemical_processing"
        )
        item["line_velocity_attention"] = (
            "large_velocity_offset_check"
            if abs(item["radial_velocity_km_s"]) > 30
            else "moderate_velocity_offset_screen"
        )
        enriched.append(item)

    return enriched


def summarize_by_environment(rows: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row["environment"], []).append(row)

    summary = []
    for environment, records in sorted(groups.items()):
        summary.append(
            {
                "environment": environment,
                "n": len(records),
                "mean_fractional_abundance": mean(row["fractional_abundance"] for row in records),
                "mean_dust_temperature_K": mean(row["dust_temperature_K"] for row in records),
                "mean_uv_field_index": mean(row["uv_field_index"] for row in records),
                "thermal_release_attention_count": sum(
                    row["thermal_release_screen"] == "thermal_release_attention"
                    for row in records
                ),
                "high_photochemical_count": sum(
                    row["photochemical_screen"] == "high_photochemical_processing"
                    for row in records
                ),
            }
        )

    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict], summary: list[dict]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    thermal = [row for row in rows if row["thermal_release_screen"] == "thermal_release_attention"]
    photochemical = [row for row in rows if row["photochemical_screen"] == "high_photochemical_processing"]
    velocity = [row for row in rows if row["line_velocity_attention"] == "large_velocity_offset_check"]

    lines = [
        "# Astrochemical Survey Screening Report",
        "",
        "This educational report summarizes synthetic astrochemical molecular-survey records.",
        "",
        f"Total records: {len(rows)}",
        f"Thermal release attention flags: {len(thermal)}",
        f"High photochemical processing flags: {len(photochemical)}",
        f"Large velocity offset checks: {len(velocity)}",
        "",
        "## Thermal release attention",
        "",
    ]

    for row in thermal:
        lines.append(
            f"- {row['source']} | {row['candidate_species']} | T_dust={row['dust_temperature_K']} K | "
            f"k_des={row['desorption_rate_s1_simplified']:.3e} s^-1"
        )

    lines.extend(["", "## High photochemical processing", ""])

    for row in photochemical:
        lines.append(
            f"- {row['source']} | {row['candidate_species']} | UV index={row['uv_field_index']} | "
            f"lifetime={row['photodissociation_lifetime_years_simplified']:.3e} years"
        )

    lines.extend(["", "## Environment summary", ""])

    for row in summary:
        lines.append(
            f"- {row['environment']} | mean abundance={row['mean_fractional_abundance']:.3e} | "
            f"mean dust T={row['mean_dust_temperature_K']:.1f} K"
        )

    lines.extend(
        [
            "",
            "This report is educational and is not a professional molecular-line identification, radiative-transfer model, mission analysis, or biosignature assessment.",
        ]
    )

    (REPORT_DIR / "astrochemical_survey_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def write_manifest() -> None:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    manifest = {
        "article_slug": "astrochemistry-molecular-universe",
        "workflow": "astrochemical_spectral_workflow.py",
        "data_source": "synthetic educational astrochemical survey data",
        "generated_outputs": [
            "outputs/tables/astrochemical_indicators.csv",
            "outputs/tables/environment_summary.csv",
            "outputs/reports/astrochemical_survey_report.md",
        ],
        "responsible_use": "Educational only; not for professional line identification, radiative transfer, mission analysis, exoplanet retrieval, biosignature assessment, or legal decisions.",
    }

    (MANIFEST_DIR / "provenance_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)

    rows = load_rows()
    indicators = add_indicators(rows)
    summary = summarize_by_environment(indicators)

    write_csv(TABLE_DIR / "astrochemical_indicators.csv", indicators)
    write_csv(TABLE_DIR / "environment_summary.csv", summary)
    write_report(indicators, summary)
    write_manifest()

    print("Astrochemical spectral workflow complete.")
    print(f"Wrote outputs to: {ARTICLE_DIR / 'outputs'}")


if __name__ == "__main__":
    main()
