# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for chemical metrology, standards, reference materials, and uncertainty.

## Core Calculations

Combined standard uncertainty:

uc = sqrt(sum(ui^2))

Expanded uncertainty:

U = k * uc

Relative uncertainty:

ur = uc / abs(x)

Bias:

bias = x_lab - x_ref

Normalized error:

En = (x_lab - x_ref) / sqrt(U_lab^2 + U_ref^2)

## Scientific Caution

These examples use simplified educational assumptions. Real chemical metrology requires validated methods, appropriate reference materials, traceability documentation, uncertainty analysis, accreditation context where applicable, and professional review.
