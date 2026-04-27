# Setup Guide

Run commands from this article directory:

articles/chemical-metrology-standards-reference-materials

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_uncertainty_budget.py
python python/02_reference_material_summary.py
python python/03_traceability_chain.py
python python/04_interlaboratory_comparison.py
python python/05_provenance_manifest.py
python python/06_generate_metrology_report.py
python python/run_all.py

## R

Rscript r/uncertainty_budget.R
Rscript r/reference_material_summary.R
Rscript r/interlaboratory_comparison.R

## Julia

julia julia/metrology_kernel.jl

## Fortran

gfortran fortran/uncertainty_kernel.f90 -o /tmp/metrology_uncertainty_kernel
/tmp/metrology_uncertainty_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/metrology_metadata_summary.go

## C

cc c/normalized_error.c -lm -o /tmp/normalized_error_c
/tmp/normalized_error_c

## C++

c++ -std=c++17 cpp/metrology_calculator.cpp -o /tmp/metrology_calculator_cpp
/tmp/metrology_calculator_cpp

## SQL

sqlite3 /tmp/chemical_metrology.db < sql/chemical_metrology_schema.sql
sqlite3 /tmp/chemical_metrology.db < sql/sample_queries.sql

## Notebook

Open notebooks/chemical_metrology_workflow.ipynb in JupyterLab or VS Code.
