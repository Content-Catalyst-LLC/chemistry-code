# Setup Guide

Run commands from this article directory:

articles/intermolecular-forces-chemistry-condensed-matter

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_lennard_jones_potential.py
python python/02_vapor_pressure_fit.py
python python/03_radial_distribution_scaffold.py
python python/04_phase_property_summary.py
python python/05_provenance_manifest.py
python python/06_generate_condensed_matter_report.py
python python/run_all.py

## R

Rscript r/vapor_pressure_fit.R
Rscript r/surface_tension_summary.R
Rscript r/phase_property_summary.R

## Julia

julia julia/intermolecular_forces_kernel.jl

## Fortran

gfortran fortran/lennard_jones_kernel.f90 -o /tmp/lennard_jones_kernel
/tmp/lennard_jones_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/condensed_matter_summary.go

## C

cc c/lennard_jones_potential.c -lm -o /tmp/lennard_jones_potential_c
/tmp/lennard_jones_potential_c

## C++

c++ -std=c++17 cpp/condensed_matter_calculator.cpp -o /tmp/condensed_matter_calculator_cpp
/tmp/condensed_matter_calculator_cpp

## SQL

sqlite3 /tmp/intermolecular_forces.db < sql/intermolecular_forces_schema.sql
sqlite3 /tmp/intermolecular_forces.db < sql/sample_queries.sql

## Notebook

Open notebooks/intermolecular_forces_workflow.ipynb in JupyterLab or VS Code.
