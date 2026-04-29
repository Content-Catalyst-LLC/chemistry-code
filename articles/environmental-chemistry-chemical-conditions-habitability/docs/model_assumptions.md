# Model Assumptions

The computational examples in this folder are intentionally simplified.

## First-order decay

The first-order decay workflow assumes:

- a pulse release
- a well-mixed compartment
- no continuing source
- a constant rate coefficient
- no explicit sorption, advection, dispersion, photochemical variation, microbial adaptation, or matrix heterogeneity

The model is useful for teaching persistence, half-life, and screening logic, but it is not a substitute for site-calibrated fate-and-transport modeling.

## Benchmark screening

The hazard quotient workflow uses:

HQ = measured concentration / benchmark concentration

HQ greater than 1 indicates that a concentration exceeds the selected benchmark. It does not prove harm. Interpretation depends on the benchmark basis, receptor, exposure route, duration, analytical uncertainty, mixture context, and decision framework.

## Acid-base speciation

The weak-acid speciation example assumes ideal behavior and a single acid dissociation constant. Real environmental systems may require activity corrections, multiple equilibria, complexation, sorption, ionic strength effects, and temperature dependence.
