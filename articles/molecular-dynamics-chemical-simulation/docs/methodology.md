# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for molecular dynamics and chemical simulation.

## Core Relationships

Newton's second law:

F_i = m_i a_i

Force from potential energy:

F_i = -grad_i U(R)

Kinetic energy:

K = sum_i 1/2 m_i v_i^2

Total energy:

E = K + U

Lennard-Jones potential:

U(r) = 4 epsilon [(sigma / r)^12 - (sigma / r)^6]

Coulomb interaction:

U(r) = q_i q_j / (4 pi epsilon_0 r)

Velocity Verlet position update:

r(t + dt) = r(t) + v(t) dt + 1/2 a(t) dt^2

Mean-squared displacement:

MSD(t) = <|r(t) - r(0)|^2>

Diffusion coefficient:

D = lim_{t->infinity} MSD(t) / 6t

Free energy from probability:

F(x) = -kBT ln P(x) + C

## Scientific Caution

These examples use simplified educational assumptions. Real molecular dynamics requires validated structures, appropriate force fields, careful system preparation, energy minimization, equilibration, production runs, sampling analysis, uncertainty estimates, and expert interpretation.
