# Setup Guide

Run commands from this article directory:

articles/oxidation-reduction-electron-transfer

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_cell_potential_gibbs.py
python python/02_nernst_equation.py
python python/03_redox_titration.py
python python/04_ph_corrosion_redox.py
python python/05_provenance_manifest.py
python python/06_generate_redox_report.py
python python/run_all.py

## R

Rscript r/cell_potential.R
Rscript r/nernst_equation.R
Rscript r/redox_titration.R
Rscript r/ph_dependent_redox.R

## Julia

julia julia/redox_kernel.jl

## Fortran

gfortran fortran/redox_kernel.f90 -o /tmp/redox_kernel
/tmp/redox_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/redox_summary.go

## C

cc c/redox_calculator.c -lm -o /tmp/redox_calculator_c
/tmp/redox_calculator_c

## C++

c++ -std=c++17 cpp/redox_calculator.cpp -o /tmp/redox_calculator_cpp
/tmp/redox_calculator_cpp

## SQL

sqlite3 /tmp/redox.db < sql/redox_schema.sql
sqlite3 /tmp/redox.db < sql/sample_queries.sql

## Notebook

Open notebooks/redox_workflow.ipynb in JupyterLab or VS Code.
