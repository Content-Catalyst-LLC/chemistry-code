# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for chemical biology and molecular intervention in living systems.

## Core Relationships

Binding equilibrium:

Kd = [P][L] / [PL]

Fractional occupancy:

theta = [L] / (Kd + [L])

Dose-response:

Response = Bottom + (Top - Bottom) / (1 + (EC50 / [L])^n)

Inhibition fraction:

I = [L]^n / (IC50^n + [L]^n)

Target engagement fraction:

TE = (Signal_control - Signal_treated) / (Signal_control - Signal_max)

Selectivity ratio:

Selectivity = Activity_off_target / Activity_target

First-order target loss:

P(t) = P0 exp(-k t)

Perturbation vector:

Delta x = x_treated - x_control

## Scientific Caution

These examples use simplified educational assumptions. Real chemical biology requires validated probes, target engagement evidence, assay controls, biological context, dose-response and time-course design, off-target assessment, toxicity checks, biosafety review, and expert interpretation.
