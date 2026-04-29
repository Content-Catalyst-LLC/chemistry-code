# Setup Guide

Run commands from this article directory:

articles/computational-chemistry-molecular-modeling

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_molecular_descriptors.py
python python/02_conformer_boltzmann.py
python python/03_potentials_similarity.py
python python/04_reaction_energy_modeling.py
python python/05_provenance_manifest.py
python python/06_generate_computational_chemistry_report.py
python python/run_all.py

## R

Rscript r/molecular_descriptors.R
Rscript r/conformer_boltzmann.R
Rscript r/lennard_jones_potential.R
Rscript r/tanimoto_similarity.R

## Julia

julia julia/computational_chemistry_kernel.jl

## Fortran

gfortran fortran/computational_chemistry_kernel.f90 -o /tmp/computational_chemistry_kernel
/tmp/computational_chemistry_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/computational_chemistry_summary.go

## C

cc c/computational_chemistry_calculator.c -lm -o /tmp/computational_chemistry_calculator_c
/tmp/computational_chemistry_calculator_c

## C++

c++ -std=c++17 cpp/computational_chemistry_calculator.cpp -o /tmp/computational_chemistry_calculator_cpp
/tmp/computational_chemistry_calculator_cpp

## SQL

sqlite3 /tmp/computational_chemistry.db < sql/computational_chemistry_schema.sql
sqlite3 /tmp/computational_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/computational_chemistry_workflow.ipynb in JupyterLab or VS Code.
