# Setup Guide

Run commands from this article directory:

articles/catalysis-control-chemical-pathways

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_barrier_rate_enhancement.py
python python/02_turnover_metrics.py
python python/03_adsorption_surface_rates.py
python python/04_catalytic_cycle_deactivation.py
python python/05_provenance_manifest.py
python python/06_generate_catalysis_report.py
python python/run_all.py

## R

Rscript r/barrier_enhancement.R
Rscript r/turnover_metrics.R
Rscript r/langmuir_surface_rate.R
Rscript r/michaelis_menten.R

## Julia

julia julia/catalysis_kernel.jl

## Fortran

gfortran fortran/catalysis_kernel.f90 -o /tmp/catalysis_kernel
/tmp/catalysis_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/catalysis_summary.go

## C

cc c/catalysis_calculator.c -lm -o /tmp/catalysis_calculator_c
/tmp/catalysis_calculator_c

## C++

c++ -std=c++17 cpp/catalysis_calculator.cpp -o /tmp/catalysis_calculator_cpp
/tmp/catalysis_calculator_cpp

## SQL

sqlite3 /tmp/catalysis.db < sql/catalysis_schema.sql
sqlite3 /tmp/catalysis.db < sql/sample_queries.sql

## Notebook

Open notebooks/catalysis_workflow.ipynb in JupyterLab or VS Code.
