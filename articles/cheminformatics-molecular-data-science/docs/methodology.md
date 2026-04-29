# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for cheminformatics and molecular data science.

## Core Relationships

Molecular graph:

G = (V, E)

Adjacency matrix:

A_ij = 1 if atoms i and j are bonded, otherwise 0

Descriptor vector:

x_i = [x_i1, x_i2, ..., x_ip]

Binary fingerprint:

f in {0, 1}^m

Tanimoto similarity:

T = c / (a + b - c)

pIC50 transformation:

pIC50 = -log10(IC50 in molar units)

QSAR scaffold:

y = f(x) + error

RMSE:

RMSE = sqrt(mean((y - y_hat)^2))

Applicability-domain distance:

D_i = min_j distance(x_i, x_j)

## Scientific Caution

These examples use simplified educational assumptions. Real cheminformatics requires validated structure parsing, standardization, stereochemistry handling, assay curation, unit normalization, leakage-aware splitting, applicability-domain analysis, uncertainty reporting, and expert interpretation.
