# Setup Guide

Run commands from this article directory:

articles/periodic-table-logic-chemical-classification

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_periodic_classification.py
python python/02_periodic_trends.py
python python/03_element_similarity.py
python python/04_atomic_weight_and_features.py
python python/05_provenance_manifest.py
python python/06_generate_periodic_classification_report.py
python python/run_all.py

## R

Rscript r/periodic_classification_summary.R
Rscript r/periodic_trend_models.R
Rscript r/isotope_weighted_mass.R

## Julia

julia julia/periodic_classification_kernel.jl

## Fortran

gfortran fortran/isotope_weight_kernel.f90 -o /tmp/isotope_weight_kernel
/tmp/isotope_weight_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/periodic_classification_summary.go

## C

cc c/periodic_similarity.c -lm -o /tmp/periodic_similarity_c
/tmp/periodic_similarity_c

## C++

c++ -std=c++17 cpp/periodic_classification_calculator.cpp -o /tmp/periodic_classification_calculator_cpp
/tmp/periodic_classification_calculator_cpp

## SQL

sqlite3 /tmp/periodic_classification.db < sql/periodic_classification_schema.sql
sqlite3 /tmp/periodic_classification.db < sql/sample_queries.sql

## Notebook

Open notebooks/periodic_classification_workflow.ipynb in JupyterLab or VS Code.
