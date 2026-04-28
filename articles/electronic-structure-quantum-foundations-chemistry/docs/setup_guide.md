# Setup Guide

Run commands from this article directory:

articles/electronic-structure-quantum-foundations-chemistry

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_hydrogen_energy_levels.py
python python/02_orbital_capacity_and_configuration.py
python python/03_particle_in_box.py
python python/04_hamiltonian_eigenproblem.py
python python/05_provenance_manifest.py
python python/06_generate_electronic_structure_report.py
python python/run_all.py

## R

Rscript r/hydrogen_energy_levels.R
Rscript r/orbital_capacity_summary.R
Rscript r/hamiltonian_eigenproblem.R

## Julia

julia julia/electronic_structure_kernel.jl

## Fortran

gfortran fortran/hydrogen_levels_kernel.f90 -o /tmp/hydrogen_levels_kernel
/tmp/hydrogen_levels_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/electronic_structure_summary.go

## C

cc c/photon_energy.c -lm -o /tmp/photon_energy_c
/tmp/photon_energy_c

## C++

c++ -std=c++17 cpp/electronic_structure_calculator.cpp -o /tmp/electronic_structure_calculator_cpp
/tmp/electronic_structure_calculator_cpp

## SQL

sqlite3 /tmp/electronic_structure.db < sql/electronic_structure_schema.sql
sqlite3 /tmp/electronic_structure.db < sql/sample_queries.sql

## Notebook

Open notebooks/electronic_structure_workflow.ipynb in JupyterLab or VS Code.
