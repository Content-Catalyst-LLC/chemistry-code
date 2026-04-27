# Setup Guide

Run commands from this article directory:

articles/chemical-revolution-rise-modern-chemistry

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_mass_conservation.py
python python/02_oxidation_mass_gain.py
python python/03_combustion_stoichiometry.py
python python/04_nomenclature_mapping.py
python python/05_provenance_manifest.py
python python/06_generate_chemical_revolution_report.py
python python/run_all.py

## R

Rscript r/mass_balance_table.R
Rscript r/oxidation_mass_gain.R
Rscript r/nomenclature_mapping.R

## Julia

julia julia/chemical_revolution_kernel.jl

## Fortran

gfortran fortran/conservation_mass_kernel.f90 -o /tmp/conservation_mass_kernel
/tmp/conservation_mass_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/chemical_revolution_metadata_summary.go

## C

cc c/oxidation_mass_gain.c -o /tmp/oxidation_mass_gain_c
/tmp/oxidation_mass_gain_c

## C++

c++ -std=c++17 cpp/chemical_revolution_calculator.cpp -o /tmp/chemical_revolution_calculator_cpp
/tmp/chemical_revolution_calculator_cpp

## SQL

sqlite3 /tmp/chemical_revolution.db < sql/chemical_revolution_schema.sql
sqlite3 /tmp/chemical_revolution.db < sql/sample_queries.sql

## Notebook

Open notebooks/chemical_revolution_workflow.ipynb in JupyterLab or VS Code.
