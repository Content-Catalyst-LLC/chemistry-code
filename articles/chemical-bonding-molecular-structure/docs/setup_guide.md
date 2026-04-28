# Setup Guide

Run commands from this article directory:

articles/chemical-bonding-molecular-structure

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_bond_geometry.py
python python/02_bond_polarity.py
python python/03_formal_charge_and_bond_order.py
python python/04_dipole_and_vsepr_summary.py
python python/05_provenance_manifest.py
python python/06_generate_bonding_report.py
python python/run_all.py

## R

Rscript r/bond_polarity.R
Rscript r/formal_charge_bond_order.R
Rscript r/molecular_geometry.R

## Julia

julia julia/bonding_kernel.jl

## Fortran

gfortran fortran/bond_order_kernel.f90 -o /tmp/bond_order_kernel
/tmp/bond_order_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/bonding_summary.go

## C

cc c/bond_geometry.c -lm -o /tmp/bond_geometry_c
/tmp/bond_geometry_c

## C++

c++ -std=c++17 cpp/bonding_calculator.cpp -o /tmp/bonding_calculator_cpp
/tmp/bonding_calculator_cpp

## SQL

sqlite3 /tmp/chemical_bonding.db < sql/chemical_bonding_schema.sql
sqlite3 /tmp/chemical_bonding.db < sql/sample_queries.sql

## Notebook

Open notebooks/chemical_bonding_workflow.ipynb in JupyterLab or VS Code.
