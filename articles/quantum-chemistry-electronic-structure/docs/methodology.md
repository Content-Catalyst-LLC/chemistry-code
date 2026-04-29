# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for quantum chemistry and electronic structure.

## Core Relationships

Schrodinger equation:

H psi = E psi

Molecular orbital expansion:

psi_i = sum_mu c_mu_i chi_mu

Electronic energy as a function of geometry:

E = E(R)

Geometry optimization condition:

grad E(R) = 0

Electron density:

rho(r) = sum_i n_i |psi_i(r)|^2

Correlation energy:

E_corr = E_exact - E_HF

DFT conceptual form:

E = E[rho]

Boltzmann electronic-state population:

p_i = exp(-E_i / R T) / sum_j exp(-E_j / R T)

Transition-state-theory scaffold:

k = kB T / h * exp(-DeltaG_dagger / R T)

Spin multiplicity:

M = 2S + 1

## Scientific Caution

These examples use simplified educational assumptions. Real quantum chemistry requires validated structures, appropriate charge and spin, method and basis-set selection, convergence diagnostics, frequency checks, benchmark comparison, uncertainty analysis, and expert interpretation.
