# Setup Guide

Run commands from this article directory:

articles/reaction-networks-chemical-systems-modeling

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_stoichiometric_matrix.py
python python/02_network_ode_simulation.py
python python/03_parallel_branching_selectivity.py
python python/04_flux_sensitivity_fitting.py
python python/05_provenance_manifest.py
python python/06_generate_network_report.py
python python/run_all.py

## R

Rscript r/stoichiometric_matrix.R
Rscript r/network_simulation.R
Rscript r/parallel_selectivity.R
Rscript r/sensitivity_analysis.R

## Julia

julia julia/reaction_network_kernel.jl

## Fortran

gfortran fortran/reaction_network_kernel.f90 -o /tmp/reaction_network_kernel
/tmp/reaction_network_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/reaction_network_summary.go

## C

cc c/reaction_network_calculator.c -lm -o /tmp/reaction_network_calculator_c
/tmp/reaction_network_calculator_c

## C++

c++ -std=c++17 cpp/reaction_network_calculator.cpp -o /tmp/reaction_network_calculator_cpp
/tmp/reaction_network_calculator_cpp

## SQL

sqlite3 /tmp/reaction_networks.db < sql/reaction_network_schema.sql
sqlite3 /tmp/reaction_networks.db < sql/sample_queries.sql

## Notebook

Open notebooks/reaction_network_workflow.ipynb in JupyterLab or VS Code.
