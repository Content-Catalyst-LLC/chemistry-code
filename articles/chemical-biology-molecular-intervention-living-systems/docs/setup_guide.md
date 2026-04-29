# Setup Guide

Run commands from this article directory:

articles/chemical-biology-molecular-intervention-living-systems

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_dose_response.py
python python/02_target_engagement_probe_quality.py
python python/03_chemoproteomics_selectivity.py
python python/04_perturbation_networks.py
python python/05_provenance_manifest.py
python python/06_generate_chemical_biology_report.py
python python/run_all.py

## R

Rscript r/dose_response.R
Rscript r/target_engagement.R
Rscript r/probe_quality.R
Rscript r/perturbation_vector.R

## Julia

julia julia/chemical_biology_kernel.jl

## Fortran

gfortran fortran/chemical_biology_kernel.f90 -o /tmp/chemical_biology_kernel
/tmp/chemical_biology_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/chemical_biology_summary.go

## C

cc c/chemical_biology_calculator.c -lm -o /tmp/chemical_biology_calculator_c
/tmp/chemical_biology_calculator_c

## C++

c++ -std=c++17 cpp/chemical_biology_calculator.cpp -o /tmp/chemical_biology_calculator_cpp
/tmp/chemical_biology_calculator_cpp

## SQL

sqlite3 /tmp/chemical_biology.db < sql/chemical_biology_schema.sql
sqlite3 /tmp/chemical_biology.db < sql/sample_queries.sql

## Notebook

Open notebooks/chemical_biology_workflow.ipynb in JupyterLab or VS Code.
