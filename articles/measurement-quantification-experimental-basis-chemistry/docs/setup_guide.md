# Setup Guide

Run commands from this article directory:

articles/measurement-quantification-experimental-basis-chemistry

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_mass_volume_concentration.py
python python/02_calibration_curve.py
python python/03_replicate_uncertainty.py
python python/04_dilution_workflow.py
python python/05_provenance_manifest.py
python python/06_generate_measurement_report.py
python python/run_all.py

## R

Rscript r/calibration_curve.R
Rscript r/replicate_uncertainty.R
Rscript r/dilution_workflow.R

## Julia

julia julia/measurement_quantification_kernel.jl

## Fortran

gfortran fortran/concentration_kernel.f90 -o /tmp/concentration_kernel
/tmp/concentration_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/measurement_metadata_summary.go

## C

cc c/uncertainty_kernel.c -lm -o /tmp/uncertainty_kernel_c
/tmp/uncertainty_kernel_c

## C++

c++ -std=c++17 cpp/measurement_calculator.cpp -o /tmp/measurement_calculator_cpp
/tmp/measurement_calculator_cpp

## SQL

sqlite3 /tmp/measurement_quantification.db < sql/measurement_quantification_schema.sql
sqlite3 /tmp/measurement_quantification.db < sql/sample_queries.sql

## Notebook

Open notebooks/measurement_quantification_workflow.ipynb in JupyterLab or VS Code.
