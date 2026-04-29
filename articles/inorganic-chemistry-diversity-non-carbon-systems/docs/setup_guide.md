# Setup Guide

Run commands from this article directory:

articles/inorganic-chemistry-diversity-non-carbon-systems

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_oxidation_states.py
python python/02_coordination_ligands.py
python python/03_crystal_field_magnetism.py
python python/04_ionic_materials_descriptors.py
python python/05_provenance_manifest.py
python python/06_generate_inorganic_report.py
python python/run_all.py

## R

Rscript r/oxidation_states.R
Rscript r/coordination_descriptors.R
Rscript r/crystal_field_magnetism.R
Rscript r/perovskite_tolerance.R

## Julia

julia julia/inorganic_kernel.jl

## Fortran

gfortran fortran/inorganic_kernel.f90 -o /tmp/inorganic_kernel
/tmp/inorganic_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/inorganic_summary.go

## C

cc c/inorganic_calculator.c -lm -o /tmp/inorganic_calculator_c
/tmp/inorganic_calculator_c

## C++

c++ -std=c++17 cpp/inorganic_calculator.cpp -o /tmp/inorganic_calculator_cpp
/tmp/inorganic_calculator_cpp

## SQL

sqlite3 /tmp/inorganic_chemistry.db < sql/inorganic_schema.sql
sqlite3 /tmp/inorganic_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/inorganic_workflow.ipynb in JupyterLab or VS Code.
