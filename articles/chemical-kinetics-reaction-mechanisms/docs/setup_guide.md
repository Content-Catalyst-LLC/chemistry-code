# Setup Guide

Run commands from this article directory:

articles/chemical-kinetics-reaction-mechanisms

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_integrated_rate_laws.py
python python/02_arrhenius_analysis.py
python python/03_reaction_mechanism_odes.py
python python/04_enzyme_kinetics.py
python python/05_provenance_manifest.py
python python/06_generate_kinetics_report.py
python python/run_all.py

## R

Rscript r/first_order_fit.R
Rscript r/arrhenius_fit.R
Rscript r/michaelis_menten_fit.R

## Julia

julia julia/kinetics_kernel.jl

## Fortran

gfortran fortran/first_order_kernel.f90 -o /tmp/first_order_kernel
/tmp/first_order_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/kinetics_summary.go

## C

cc c/kinetics_calculator.c -lm -o /tmp/kinetics_calculator_c
/tmp/kinetics_calculator_c

## C++

c++ -std=c++17 cpp/kinetics_calculator.cpp -o /tmp/kinetics_calculator_cpp
/tmp/kinetics_calculator_cpp

## SQL

sqlite3 /tmp/chemical_kinetics.db < sql/kinetics_schema.sql
sqlite3 /tmp/chemical_kinetics.db < sql/sample_queries.sql

## Notebook

Open notebooks/chemical_kinetics_workflow.ipynb in JupyterLab or VS Code.
