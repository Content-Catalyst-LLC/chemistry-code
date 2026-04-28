# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for chemical thermodynamics and energetics.

## Core Relationships

First law:

Delta U = q + w

Pressure-volume work:

w = -P_ext Delta V

Enthalpy:

H = U + pV

Constant-pressure heat:

q_p = Delta H

Calorimetry:

q = m c Delta T

Hess's law:

Delta H overall = sum(Delta H_i)

Standard reaction enthalpy:

Delta H rxn = sum(nu products Delta Hf products) - sum(nu reactants Delta Hf reactants)

Gibbs free energy:

Delta G = Delta H - T Delta S

Free energy under nonstandard conditions:

Delta G = Delta G standard + R T ln Q

Free energy and equilibrium:

Delta G standard = -R T ln K

van 't Hoff relationship:

ln K = -Delta H standard / (R T) + Delta S standard / R

## Scientific Caution

These examples use simplified educational assumptions. Real thermodynamic work requires evaluated reference data, clear standard states, phase specification, unit control, uncertainty analysis, activity corrections when needed, and expert interpretation.
