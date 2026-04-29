# Setup Guide

Run commands from this article directory:

articles/r-chemistry-statistics-experimental-analysis

## R

User preference: pak is recommended for R package installation.

Install dependencies if needed:

install.packages("pak")
pak::pak(c("tidyverse", "broom", "readr", "dplyr", "ggplot2", "tibble"))

Run:

Rscript r/01_replicate_summary.R
Rscript r/02_calibration_curve.R
Rscript r/03_kinetics_arrhenius.R
Rscript r/04_anova_qc.R
Rscript r/05_generate_r_chemistry_report.R

## Python

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy scipy matplotlib

Run:

python python/replicate_summary.py
python python/calibration_statistics.py
python python/kinetics_statistics.py
python python/provenance_manifest.py

## Julia

julia julia/r_chemistry_kernel.jl

## Fortran

gfortran fortran/r_chemistry_kernel.f90 -o /tmp/r_chemistry_kernel
/tmp/r_chemistry_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/r_chemistry_summary.go

## C

cc c/r_chemistry_calculator.c -lm -o /tmp/r_chemistry_calculator_c
/tmp/r_chemistry_calculator_c

## C++

c++ -std=c++17 cpp/r_chemistry_calculator.cpp -o /tmp/r_chemistry_calculator_cpp
/tmp/r_chemistry_calculator_cpp

## SQL

sqlite3 /tmp/r_chemistry.db < sql/r_chemistry_schema.sql
sqlite3 /tmp/r_chemistry.db < sql/sample_queries.sql

## Notebook

Open notebooks/r_chemistry_workflow.ipynb in JupyterLab or VS Code.
