# Setup Guide

Run commands from this article directory:

articles/cheminformatics-molecular-data-science

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_descriptors_graphs.py
python python/02_fingerprints_similarity.py
python python/03_assay_standardization.py
python python/04_splits_applicability_modeling.py
python python/05_provenance_manifest.py
python python/06_generate_cheminformatics_report.py
python python/run_all.py

## R

Rscript r/descriptors.R
Rscript r/tanimoto_similarity.R
Rscript r/pic50_standardization.R
Rscript r/applicability_domain.R

## Julia

julia julia/cheminformatics_kernel.jl

## Fortran

gfortran fortran/cheminformatics_kernel.f90 -o /tmp/cheminformatics_kernel
/tmp/cheminformatics_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/cheminformatics_summary.go

## C

cc c/cheminformatics_calculator.c -lm -o /tmp/cheminformatics_calculator_c
/tmp/cheminformatics_calculator_c

## C++

c++ -std=c++17 cpp/cheminformatics_calculator.cpp -o /tmp/cheminformatics_calculator_cpp
/tmp/cheminformatics_calculator_cpp

## SQL

sqlite3 /tmp/cheminformatics.db < sql/cheminformatics_schema.sql
sqlite3 /tmp/cheminformatics.db < sql/sample_queries.sql

## Notebook

Open notebooks/cheminformatics_workflow.ipynb in JupyterLab or VS Code.
