# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for R-centered chemical statistics and experimental analysis.

## Core Relationships

Mean:

x_bar = sum(x_i) / n

Sample standard deviation:

s = sqrt(sum((x_i - x_bar)^2) / (n - 1))

Standard error:

SE = s / sqrt(n)

Relative standard deviation:

RSD = s / x_bar * 100%

Linear calibration:

y = m x + b

Unknown concentration:

x = (y - b) / m

Residual:

r_i = y_i - y_hat_i

RMSE:

RMSE = sqrt(mean((y_i - y_hat_i)^2))

First-order kinetics:

C(t) = C0 exp(-k t)

Arrhenius linear form:

ln(k) = ln(A) - Ea / R * 1 / T

One-way ANOVA:

y_ij = mu + alpha_i + epsilon_ij

Detection-limit approximation:

LOD = 3 s_b / m

Quantification-limit approximation:

LOQ = 10 s_b / m

## Scientific Caution

These examples use simplified educational assumptions. Real chemical analysis requires validated analytical methods, calibrated instruments, documented sample preparation, quality-control standards, appropriate statistical assumptions, uncertainty budgets, and expert chemical interpretation.
