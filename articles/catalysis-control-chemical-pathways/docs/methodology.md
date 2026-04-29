# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for catalysis and pathway-control systems.

## Core Relationships

Arrhenius equation:

k = A exp(-Ea / R T)

Barrier-lowering rate estimate:

k_cat / k_uncat approx exp(Delta Ea / R T)

Turnover number:

TON = moles product / moles catalyst

Turnover frequency:

TOF = TON / time

Michaelis-Menten equation:

v = Vmax [S] / (Km + [S])

Langmuir adsorption:

theta = K P / (1 + K P)

Langmuir-Hinshelwood surface rate:

r = k theta_A theta_B

Catalytic-cycle ODE form:

dc/dt = S r(c,T)

## Scientific Caution

These examples use simplified educational assumptions. Real catalytic analysis requires validated kinetics, catalyst characterization, transport checks, deactivation assessment, uncertainty analysis, safety review, and expert interpretation.
