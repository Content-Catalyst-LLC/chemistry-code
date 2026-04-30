# Advanced Model Notes: Ocean Chemistry and the Carbonate System

This advanced layer is designed to make the GitHub repository more credible as a computational science companion to the article.

## What this layer adds

- carbonate speciation from pH and DIC
- CO2*, bicarbonate, and carbonate ion estimates
- aragonite and calcite saturation-state screening
- air-sea CO2 flux proxy
- alkalinity-DIC buffer ratio
- Revelle-factor intuition proxy
- acidification-pressure index
- DIC perturbation sensitivity series
- SQL-ready provenance structure
- lightweight tests

## Important simplifications

The workflow uses fixed educational constants for carbonate chemistry. Real ocean carbonate chemistry requires:

- temperature-dependent equilibrium constants
- salinity-dependent equilibrium constants
- pressure corrections
- pH scale conversion
- nutrient corrections
- borate alkalinity
- certified reference materials
- uncertainty propagation
- validated software such as CO2SYS, PyCO2SYS, seacarb, or equivalent tools

## Interpretation

The output indices are screening and teaching indicators. They help explain carbonate-system logic but should not be treated as scientific findings.

## Responsible-use boundary

Do not use these outputs for shellfish-hatchery decisions, marine management, reef conservation policy, legal evidence, regulatory reporting, climate attribution, or operational monitoring.
