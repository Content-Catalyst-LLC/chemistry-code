# Setup Guide

Run commands from this article directory:

articles/what-is-chemistry

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_moles_molarity_dilution.py
python python/02_first_order_kinetics.py
python python/03_beer_lambert_calibration.py
python python/04_ph_calculations.py
python python/05_provenance_manifest.py
python python/06_generate_chemistry_report.py
python python/run_all.py

## R

Rscript r/beer_lambert_calibration.R
Rscript r/ph_calculations.R
Rscript r/stoichiometry_table.R

## Julia

julia julia/chemistry_intro_kernel.jl

## Fortran

gfortran fortran/moles_molarity_kernel.f90 -o /tmp/moles_molarity_kernel
/tmp/moles_molarity_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/chemistry_metadata_summary.go

## C

cc c/first_order_kinetics.c -lm -o /tmp/first_order_kinetics_c
/tmp/first_order_kinetics_c

## C++

c++ -std=c++17 cpp/chemistry_intro_calculator.cpp -o /tmp/chemistry_intro_calculator_cpp
/tmp/chemistry_intro_calculator_cpp

## SQL

sqlite3 /tmp/what_is_chemistry.db < sql/what_is_chemistry_schema.sql
sqlite3 /tmp/what_is_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/what_is_chemistry_workflow.ipynb in JupyterLab or VS Code.
