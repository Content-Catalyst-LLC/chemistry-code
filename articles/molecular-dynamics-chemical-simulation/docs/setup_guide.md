# Setup Guide

Run commands from this article directory:

articles/molecular-dynamics-chemical-simulation

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_velocity_verlet.py
python python/02_potentials.py
python python/03_trajectory_analysis.py
python python/04_rdf_ensemble_metadata.py
python python/05_provenance_manifest.py
python python/06_generate_md_report.py
python python/run_all.py

## R

Rscript r/velocity_verlet.R
Rscript r/lennard_jones_potential.R
Rscript r/msd_diffusion.R
Rscript r/rdf_histogram.R

## Julia

julia julia/molecular_dynamics_kernel.jl

## Fortran

gfortran fortran/molecular_dynamics_kernel.f90 -o /tmp/molecular_dynamics_kernel
/tmp/molecular_dynamics_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/molecular_dynamics_summary.go

## C

cc c/molecular_dynamics_calculator.c -lm -o /tmp/molecular_dynamics_calculator_c
/tmp/molecular_dynamics_calculator_c

## C++

c++ -std=c++17 cpp/molecular_dynamics_calculator.cpp -o /tmp/molecular_dynamics_calculator_cpp
/tmp/molecular_dynamics_calculator_cpp

## SQL

sqlite3 /tmp/molecular_dynamics.db < sql/molecular_dynamics_schema.sql
sqlite3 /tmp/molecular_dynamics.db < sql/sample_queries.sql

## Notebook

Open notebooks/molecular_dynamics_workflow.ipynb in JupyterLab or VS Code.
