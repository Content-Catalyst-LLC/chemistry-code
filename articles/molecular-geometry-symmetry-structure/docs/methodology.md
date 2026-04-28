# Methodology Notes

## Purpose

This repository demonstrates reproducible computational scaffolding for molecular geometry, symmetry, and structure.

## Core Relationships

Atomic coordinate:

r_i = (x_i, y_i, z_i)

Bond distance:

d_ij = sqrt((x_i - x_j)^2 + (y_i - y_j)^2 + (z_i - z_j)^2)

Bond angle:

cos(theta) = dot(u, v) / (norm(u) * norm(v))

Center of geometry:

r_center = sum(r_i) / N

Center of mass:

r_cm = sum(m_i * r_i) / sum(m_i)

RMSD:

RMSD = sqrt(mean(sum((r_i - r'_i)^2)))

Rotation around z-axis:

Rz(theta) = [[cos theta, -sin theta, 0], [sin theta, cos theta, 0], [0, 0, 1]]

## Scientific Caution

These examples use simplified educational assumptions. Real molecular-structure work requires validated structures, clear units, experimental evidence, chemically meaningful models, uncertainty analysis, and professional review.
