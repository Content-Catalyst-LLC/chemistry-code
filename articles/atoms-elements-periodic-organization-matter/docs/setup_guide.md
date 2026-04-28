# Setup Guide

Run commands from this article directory:

articles/atoms-elements-periodic-organization-matter

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_element_features.py
python python/02_isotope_weighted_mass.py
python python/03_periodic_trends.py
python python/04_mole_and_composition.py
python python/05_provenance_manifest.py
python python/06_generate_periodic_report.py
python python/run_all.py

## R

Rscript r/isotope_weighted_mass.R
Rscript r/periodic_trend_models.R
Rscript r/mole_and_composition.R

## Julia

julia julia/periodic_kernel.jl

## Fortran

gfortran fortran/isotope_mass_kernel.f90 -o /tmp/isotope_mass_kernel
/tmp/isotope_mass_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/periodic_metadata_summary.go

## C

cc c/atomic_identity.c -lm -o /tmp/atomic_identity_c
/tmp/atomic_identity_c

## C++

c++ -std=c++17 cpp/periodic_calculator.cpp -o /tmp/periodic_calculator_cpp
/tmp/periodic_calculator_cpp

## SQL

sqlite3 /tmp/atoms_elements_periodic.db < sql/atoms_elements_periodic_schema.sql
sqlite3 /tmp/atoms_elements_periodic.db < sql/sample_queries.sql

## Notebook

Open notebooks/atoms_elements_periodic_workflow.ipynb in JupyterLab or VS Code.
