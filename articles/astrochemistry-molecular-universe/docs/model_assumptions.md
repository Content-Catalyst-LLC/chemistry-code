# Model Assumptions

The computational examples in this folder are simplified teaching tools.

## Doppler velocity

The velocity calculation uses a nonrelativistic Doppler approximation:

delta_nu / nu0 ≈ -v / c

Professional spectral analysis must specify velocity frame, uncertainty, calibration, rest-frequency source, line blending, and source structure.

## Molecular abundance

Fractional abundance is calculated as:

X = N(species) / N(H2)

This assumes column densities are compatible and representative of the same beam and physical component. Real abundance analysis requires excitation, optical depth, beam filling, radiative transfer, isotopologues, and physical modeling.

## Thermal desorption

The desorption expression uses:

k_des = nu0 exp(-Eb / T)

Binding energies, diffusion barriers, grain morphology, ice composition, and heating history strongly affect real desorption behavior.

## Photodissociation

The photodissociation lifetime is a simple UV-scaled rate. Real photochemistry depends on shielding, wavelength-dependent cross sections, dust extinction, self-shielding, cosmic rays, and radiation geometry.

## Line identification

The line matching examples are not molecule detections. Real identification requires multiple transitions, line intensity consistency, catalog uncertainty, source velocity, blending analysis, and chemical plausibility.
