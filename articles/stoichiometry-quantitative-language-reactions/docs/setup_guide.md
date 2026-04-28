# Setup Guide

Run commands from this article directory:

articles/stoichiometry-quantitative-language-reactions

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_limiting_reagent_yield.py
python python/02_solution_titration_gas.py
python python/03_empirical_formula_combustion.py
python python/04_reaction_extent_balances.py
python python/05_provenance_manifest.py
python python/06_generate_stoichiometry_report.py
python python/run_all.py

## R

Rscript r/empirical_formula.R
Rscript r/gas_stoichiometry.R
Rscript r/titration_equivalence.R

## Julia

julia julia/stoichiometry_kernel.jl

## Fortran

gfortran fortran/limiting_reagent_kernel.f90 -o /tmp/limiting_reagent_kernel
/tmp/limiting_reagent_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/stoichiometry_summary.go

## C

cc c/stoichiometry_calculator.c -lm -o /tmp/stoichiometry_calculator_c
/tmp/stoichiometry_calculator_c

## C++

c++ -std=c++17 cpp/stoichiometry_calculator.cpp -o /tmp/stoichiometry_calculator_cpp
/tmp/stoichiometry_calculator_cpp

## SQL

sqlite3 /tmp/stoichiometry.db < sql/stoichiometry_schema.sql
sqlite3 /tmp/stoichiometry.db < sql/sample_queries.sql

## Notebook

Open notebooks/stoichiometry_workflow.ipynb in JupyterLab or VS Code.
