# Advanced Model Notes

This advanced layer is designed to make the GitHub repository look and feel more like a serious computational science project while remaining honest about its limits.

## What is more advanced here?

Compared with the basic article scaffold, this layer adds:

1. reusable Python functions
2. dataclass-based line catalog objects
3. frequency-based line matching
4. Doppler velocity estimation
5. synthetic Gaussian spectral profiles
6. rotational-diagram temperature estimation
7. thermal desorption rate calculations
8. photodissociation lifetime calculations
9. a toy reaction-network integrator
10. SQL provenance structures for line matching and model runs
11. lightweight tests

## What is still simplified?

This is not a radiative-transfer code. It does not include:

- non-LTE excitation
- optical-depth correction
- molecular partition functions
- beam dilution
- hyperfine structure
- line blending
- uncertainty propagation
- catalog uncertainty
- continuum subtraction
- exoplanet retrieval
- full grain-surface chemistry
- professional astrochemical networks

## Why include it?

The goal is to demonstrate that the article has a reproducible computational backbone, with enough sophistication to show real computational thinking: spectral evidence, chemical kinetics, molecular abundance, surface chemistry, and provenance.
