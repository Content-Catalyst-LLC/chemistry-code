# Setup Guide

Run commands from this article directory:

articles/equilibrium-dynamics-reversible-systems

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_reaction_quotient_free_energy.py
python python/02_equilibrium_solver.py
python python/03_reversible_dynamics.py
python python/04_vant_hoff_solubility_activity.py
python python/05_provenance_manifest.py
python python/06_generate_equilibrium_report.py
python python/run_all.py

## R

Rscript r/reversible_dynamics.R
Rscript r/vant_hoff_fit.R
Rscript r/solubility_product.R

## Julia

julia julia/equilibrium_kernel.jl

## Fortran

gfortran fortran/equilibrium_kernel.f90 -o /tmp/equilibrium_kernel
/tmp/equilibrium_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/equilibrium_summary.go

## C

cc c/equilibrium_calculator.c -lm -o /tmp/equilibrium_calculator_c
/tmp/equilibrium_calculator_c

## C++

c++ -std=c++17 cpp/equilibrium_calculator.cpp -o /tmp/equilibrium_calculator_cpp
/tmp/equilibrium_calculator_cpp

## SQL

sqlite3 /tmp/chemical_equilibrium.db < sql/equilibrium_schema.sql
sqlite3 /tmp/chemical_equilibrium.db < sql/sample_queries.sql

## Notebook

Open notebooks/equilibrium_workflow.ipynb in JupyterLab or VS Code.
