# Setup Guide

Run commands from this article directory:

articles/mathematics-chemistry-molecular-systems

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_stoichiometry_and_ph.py
python python/02_kinetics_and_thermodynamics.py
python python/03_molecular_geometry.py
python python/04_linear_algebra_and_uncertainty.py
python python/05_provenance_manifest.py
python python/06_generate_math_chemistry_report.py
python python/run_all.py

## R

Rscript r/thermodynamics_equilibrium.R
Rscript r/calibration_uncertainty.R
Rscript r/molecular_geometry.R

## Julia

julia julia/mathematical_chemistry_kernel.jl

## Fortran

gfortran fortran/kinetics_kernel.f90 -o /tmp/kinetics_kernel
/tmp/kinetics_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/math_chemistry_metadata_summary.go

## C

cc c/stoichiometry_ph.c -lm -o /tmp/stoichiometry_ph_c
/tmp/stoichiometry_ph_c

## C++

c++ -std=c++17 cpp/math_chemistry_calculator.cpp -o /tmp/math_chemistry_calculator_cpp
/tmp/math_chemistry_calculator_cpp

## SQL

sqlite3 /tmp/mathematics_chemistry.db < sql/mathematics_chemistry_schema.sql
sqlite3 /tmp/mathematics_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/mathematics_chemistry_workflow.ipynb in JupyterLab or VS Code.
