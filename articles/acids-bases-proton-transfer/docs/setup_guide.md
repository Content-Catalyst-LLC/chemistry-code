# Setup Guide

Run commands from this article directory:

articles/acids-bases-proton-transfer

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_weak_acid_base_ph.py
python python/02_buffer_henderson_hasselbalch.py
python python/03_titration_curves.py
python python/04_speciation_polyprotic.py
python python/05_provenance_manifest.py
python python/06_generate_acid_base_report.py
python python/run_all.py

## R

Rscript r/weak_acid_ph.R
Rscript r/buffer_ph.R
Rscript r/titration_curve.R
Rscript r/speciation.R

## Julia

julia julia/acid_base_kernel.jl

## Fortran

gfortran fortran/weak_acid_kernel.f90 -o /tmp/weak_acid_kernel
/tmp/weak_acid_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/acid_base_summary.go

## C

cc c/acid_base_calculator.c -lm -o /tmp/acid_base_calculator_c
/tmp/acid_base_calculator_c

## C++

c++ -std=c++17 cpp/acid_base_calculator.cpp -o /tmp/acid_base_calculator_cpp
/tmp/acid_base_calculator_cpp

## SQL

sqlite3 /tmp/acids_bases.db < sql/acid_base_schema.sql
sqlite3 /tmp/acids_bases.db < sql/sample_queries.sql

## Notebook

Open notebooks/acid_base_workflow.ipynb in JupyterLab or VS Code.
