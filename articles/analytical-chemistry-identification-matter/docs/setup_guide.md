# Setup Guide

Run commands from this article directory:

articles/analytical-chemistry-identification-matter

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_calibration_lod_loq.py
python python/02_precision_recovery_qc.py
python python/03_chromatography_spectroscopy.py
python python/04_spectral_matching_reporting.py
python python/05_provenance_manifest.py
python python/06_generate_analytical_report.py
python python/run_all.py

## R

Rscript r/calibration_lod_loq.R
Rscript r/precision_recovery.R
Rscript r/chromatographic_resolution.R
Rscript r/beer_lambert_quantification.R

## Julia

julia julia/analytical_kernel.jl

## Fortran

gfortran fortran/analytical_kernel.f90 -o /tmp/analytical_kernel
/tmp/analytical_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/analytical_summary.go

## C

cc c/analytical_calculator.c -lm -o /tmp/analytical_calculator_c
/tmp/analytical_calculator_c

## C++

c++ -std=c++17 cpp/analytical_calculator.cpp -o /tmp/analytical_calculator_cpp
/tmp/analytical_calculator_cpp

## SQL

sqlite3 /tmp/analytical_chemistry.db < sql/analytical_schema.sql
sqlite3 /tmp/analytical_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/analytical_workflow.ipynb in JupyterLab or VS Code.
