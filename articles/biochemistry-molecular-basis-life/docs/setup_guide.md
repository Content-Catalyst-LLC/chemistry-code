# Setup Guide

Run commands from this article directory:

articles/biochemistry-molecular-basis-life

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_enzyme_kinetics.py
python python/02_binding_occupancy.py
python python/03_sequence_composition.py
python python/04_metabolic_networks.py
python python/05_provenance_manifest.py
python python/06_generate_biochemistry_report.py
python python/run_all.py

## R

Rscript r/enzyme_kinetics.R
Rscript r/binding_occupancy.R
Rscript r/sequence_composition.R
Rscript r/metabolic_flux_check.R

## Julia

julia julia/biochemistry_kernel.jl

## Fortran

gfortran fortran/biochemistry_kernel.f90 -o /tmp/biochemistry_kernel
/tmp/biochemistry_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/biochemistry_summary.go

## C

cc c/biochemistry_calculator.c -lm -o /tmp/biochemistry_calculator_c
/tmp/biochemistry_calculator_c

## C++

c++ -std=c++17 cpp/biochemistry_calculator.cpp -o /tmp/biochemistry_calculator_cpp
/tmp/biochemistry_calculator_cpp

## SQL

sqlite3 /tmp/biochemistry.db < sql/biochemistry_schema.sql
sqlite3 /tmp/biochemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/biochemistry_workflow.ipynb in JupyterLab or VS Code.
