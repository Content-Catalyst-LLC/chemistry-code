# Setup Guide

Run commands from this article directory:

articles/python-chemistry-simulation-laboratory-data

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib scipy

Run:

python python/01_calibration_curve.py
python python/02_kinetics_analysis.py
python python/03_uncertainty_qc.py
python python/04_simulation_workflow.py
python python/05_provenance_manifest.py
python python/06_generate_python_chemistry_report.py
python python/run_all.py

## R

Rscript r/calibration_curve.R
Rscript r/kinetics_analysis.R
Rscript r/replicate_summary.R
Rscript r/arrhenius_transform.R

## Julia

julia julia/python_chemistry_kernel.jl

## Fortran

gfortran fortran/python_chemistry_kernel.f90 -o /tmp/python_chemistry_kernel
/tmp/python_chemistry_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/python_chemistry_summary.go

## C

cc c/python_chemistry_calculator.c -lm -o /tmp/python_chemistry_calculator_c
/tmp/python_chemistry_calculator_c

## C++

c++ -std=c++17 cpp/python_chemistry_calculator.cpp -o /tmp/python_chemistry_calculator_cpp
/tmp/python_chemistry_calculator_cpp

## SQL

sqlite3 /tmp/python_chemistry.db < sql/python_chemistry_schema.sql
sqlite3 /tmp/python_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/python_chemistry_workflow.ipynb in JupyterLab or VS Code.
