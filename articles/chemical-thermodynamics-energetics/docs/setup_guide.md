# Setup Guide

Run commands from this article directory:

articles/chemical-thermodynamics-energetics

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_calorimetry_enthalpy.py
python python/02_hess_law_formation_enthalpy.py
python python/03_gibbs_equilibrium.py
python python/04_vant_hoff_phase_coupling.py
python python/05_provenance_manifest.py
python python/06_generate_thermodynamics_report.py
python python/run_all.py

## R

Rscript r/hess_law.R
Rscript r/gibbs_equilibrium.R
Rscript r/vant_hoff_fit.R

## Julia

julia julia/thermodynamics_kernel.jl

## Fortran

gfortran fortran/gibbs_equilibrium_kernel.f90 -o /tmp/gibbs_equilibrium_kernel
/tmp/gibbs_equilibrium_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/thermodynamics_summary.go

## C

cc c/thermodynamics_calculator.c -lm -o /tmp/thermodynamics_calculator_c
/tmp/thermodynamics_calculator_c

## C++

c++ -std=c++17 cpp/thermodynamics_calculator.cpp -o /tmp/thermodynamics_calculator_cpp
/tmp/thermodynamics_calculator_cpp

## SQL

sqlite3 /tmp/chemical_thermodynamics.db < sql/thermodynamics_schema.sql
sqlite3 /tmp/chemical_thermodynamics.db < sql/sample_queries.sql

## Notebook

Open notebooks/chemical_thermodynamics_workflow.ipynb in JupyterLab or VS Code.
