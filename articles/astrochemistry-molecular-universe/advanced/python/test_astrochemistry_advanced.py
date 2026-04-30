#!/usr/bin/env python3
"""
Lightweight tests for the advanced astrochemistry module.

Run from the advanced/python folder:

python3 test_astrochemistry_advanced.py
"""

from astrochemistry_advanced import (
    radial_velocity_km_s,
    fractional_abundance,
    thermal_desorption_rate_s1,
    photodissociation_lifetime_years,
    rotational_diagram_temperature,
)


def assert_close(value, expected, tolerance):
    assert abs(value - expected) <= tolerance, f"{value} != {expected} within {tolerance}"


def test_radial_velocity():
    velocity = radial_velocity_km_s(115.271, 115.269)
    assert velocity > 0
    assert velocity < 10


def test_fractional_abundance():
    assert_close(fractional_abundance(2.0e17, 2.0e22), 1.0e-5, 1.0e-12)


def test_desorption_rate_positive():
    rate = thermal_desorption_rate_s1(855, 30)
    assert rate > 0


def test_photodissociation_lifetime_positive():
    lifetime = photodissociation_lifetime_years(10)
    assert lifetime > 0


def test_rotational_diagram():
    result = rotational_diagram_temperature([
        {"upper_energy_K": 7.0, "g_upper": 5, "integrated_intensity_K_km_s": 39.4},
        {"upper_energy_K": 13.94, "g_upper": 7, "integrated_intensity_K_km_s": 32.7},
        {"upper_energy_K": 23.20, "g_upper": 9, "integrated_intensity_K_km_s": 22.3},
    ])
    assert result["rotational_temperature_K"] > 0


if __name__ == "__main__":
    test_radial_velocity()
    test_fractional_abundance()
    test_desorption_rate_positive()
    test_photodissociation_lifetime_positive()
    test_rotational_diagram()
    print("All advanced astrochemistry tests passed.")
