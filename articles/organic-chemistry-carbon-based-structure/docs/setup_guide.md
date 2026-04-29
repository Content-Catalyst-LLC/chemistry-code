# Setup Guide

Run commands from this article directory:

articles/organic-chemistry-carbon-based-structure

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_formula_descriptors.py
python python/02_molecular_graphs.py
python python/03_functional_groups_stereochemistry.py
python python/04_structure_property_scaffold.py
python python/05_provenance_manifest.py
python python/06_generate_organic_structure_report.py
python python/run_all.py

## R

Rscript r/formula_descriptors.R
Rscript r/functional_group_descriptors.R
Rscript r/structure_property_score.R
Rscript r/stereochemistry_scaffold.R

## Julia

julia julia/organic_structure_kernel.jl

## Fortran

gfortran fortran/organic_structure_kernel.f90 -o /tmp/organic_structure_kernel
/tmp/organic_structure_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/organic_structure_summary.go

## C

cc c/organic_structure_calculator.c -lm -o /tmp/organic_structure_calculator_c
/tmp/organic_structure_calculator_c

## C++

c++ -std=c++17 cpp/organic_structure_calculator.cpp -o /tmp/organic_structure_calculator_cpp
/tmp/organic_structure_calculator_cpp

## SQL

sqlite3 /tmp/organic_structure.db < sql/organic_structure_schema.sql
sqlite3 /tmp/organic_structure.db < sql/sample_queries.sql

## Notebook

Open notebooks/organic_structure_workflow.ipynb in JupyterLab or VS Code.
