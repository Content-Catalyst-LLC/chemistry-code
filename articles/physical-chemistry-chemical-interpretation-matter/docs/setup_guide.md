# Setup Guide

Run commands from this article directory:

articles/physical-chemistry-chemical-interpretation-matter

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_thermodynamics_equilibrium.py
python python/02_arrhenius_kinetics.py
python python/03_boltzmann_diffusion.py
python python/04_electrochemistry_transport.py
python python/05_provenance_manifest.py
python python/06_generate_physical_chemistry_report.py
python python/run_all.py

## R

Rscript r/equilibrium_constants.R
Rscript r/arrhenius_kinetics.R
Rscript r/boltzmann_populations.R
Rscript r/diffusion_scaffold.R

## Julia

julia julia/physical_chemistry_kernel.jl

## Fortran

gfortran fortran/physical_chemistry_kernel.f90 -o /tmp/physical_chemistry_kernel
/tmp/physical_chemistry_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/physical_chemistry_summary.go

## C

cc c/physical_chemistry_calculator.c -lm -o /tmp/physical_chemistry_calculator_c
/tmp/physical_chemistry_calculator_c

## C++

c++ -std=c++17 cpp/physical_chemistry_calculator.cpp -o /tmp/physical_chemistry_calculator_cpp
/tmp/physical_chemistry_calculator_cpp

## SQL

sqlite3 /tmp/physical_chemistry.db < sql/physical_chemistry_schema.sql
sqlite3 /tmp/physical_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/physical_chemistry_workflow.ipynb in JupyterLab or VS Code.
