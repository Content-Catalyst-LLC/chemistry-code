# Setup Guide

Run commands from this article directory:

articles/quantum-chemistry-electronic-structure

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_orbital_mixing.py
python python/02_density_huckel.py
python python/03_basis_spin_states.py
python python/04_excited_states_tst.py
python python/05_provenance_manifest.py
python python/06_generate_quantum_chemistry_report.py
python python/run_all.py

## R

Rscript r/orbital_mixing.R
Rscript r/basis_convergence.R
Rscript r/spin_state_comparison.R
Rscript r/transition_state_theory.R

## Julia

julia julia/quantum_chemistry_kernel.jl

## Fortran

gfortran fortran/quantum_chemistry_kernel.f90 -o /tmp/quantum_chemistry_kernel
/tmp/quantum_chemistry_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/quantum_chemistry_summary.go

## C

cc c/quantum_chemistry_calculator.c -lm -o /tmp/quantum_chemistry_calculator_c
/tmp/quantum_chemistry_calculator_c

## C++

c++ -std=c++17 cpp/quantum_chemistry_calculator.cpp -o /tmp/quantum_chemistry_calculator_cpp
/tmp/quantum_chemistry_calculator_cpp

## SQL

sqlite3 /tmp/quantum_chemistry.db < sql/quantum_chemistry_schema.sql
sqlite3 /tmp/quantum_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/quantum_chemistry_workflow.ipynb in JupyterLab or VS Code.
