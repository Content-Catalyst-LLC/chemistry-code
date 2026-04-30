# Advanced Model Notes: Medicinal Chemistry and Drug Discovery

This advanced layer is designed to make the GitHub repository more credible as a computational science companion to the article and more useful to professional medicinal chemistry readers.

## What this layer adds

- potency conversion from IC50 to pIC50
- selectivity-window calculations
- ligand efficiency proxy
- lipophilic ligand efficiency
- Lipinski-style property checks
- Veber-style property checks
- solubility scoring
- permeability scoring
- microsomal stability scoring
- hERG liability screening
- CYP3A4 inhibition screening
- plasma protein binding risk proxy
- clearance and volume-of-distribution intuition
- oral-property score
- safety-liability score
- developability score
- multiparameter optimization score
- Monte Carlo advancement probability
- Pareto frontier analysis
- potency-lipophilicity tradeoff scenario
- ADMET rescue scenario
- assay progression matrix
- SQL-ready provenance structure
- lightweight tests

## Important simplifications

The workflow is intentionally educational. It does not include:

- actual molecular graph parsing
- RDKit molecular descriptors
- 3D conformer generation
- docking
- free-energy perturbation
- QSAR model training
- pharmacophore modeling
- matched molecular pair analysis
- retrosynthesis
- synthesis route generation
- controlled-substance design
- toxicology determination
- clinical exposure prediction
- human dose prediction
- regulatory-grade safety assessment
- patient-level treatment guidance
- validated ADMET prediction
- validated PK/PD modeling
- experimental assay protocols

## Interpretation

The output indices are screening and teaching indicators. They help explain how medicinal chemistry balances potency, selectivity, physicochemical properties, ADMET, safety liabilities, developability, and decision risk, but they are not discovery decisions, toxicology findings, clinical recommendations, or regulatory conclusions.

## Responsible-use boundary

Do not use these outputs for patient care, dosing, clinical decision-making, synthesis planning, controlled-substance design, toxicology clearance, regulatory filing, investment decisions, legal evidence, or claims about real compound safety or efficacy.
