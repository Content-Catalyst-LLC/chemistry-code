# Setup Guide

Run commands from this article directory:

articles/molecular-geometry-symmetry-structure

## Python

Recommended:

python3 -m venv .venv
source .venv/bin/activate
pip install pandas numpy matplotlib

Run:

python python/01_distance_matrix_and_angles.py
python python/02_centers_and_extents.py
python python/03_rotation_and_symmetry_operation.py
python python/04_conformer_rmsd_and_torsion.py
python python/05_provenance_manifest.py
python python/06_generate_geometry_report.py
python python/run_all.py

## R

Rscript r/center_of_mass.R
Rscript r/rmsd_conformers.R
Rscript r/vsepr_summary.R

## Julia

julia julia/geometry_symmetry_kernel.jl

## Fortran

gfortran fortran/distance_kernel.f90 -o /tmp/distance_kernel
/tmp/distance_kernel

## Rust

cd rust
cargo run
cd ..

## Go

go run go/geometry_summary.go

## C

cc c/geometry_calculator.c -lm -o /tmp/geometry_calculator_c
/tmp/geometry_calculator_c

## C++

c++ -std=c++17 cpp/geometry_symmetry_calculator.cpp -o /tmp/geometry_symmetry_calculator_cpp
/tmp/geometry_symmetry_calculator_cpp

## SQL

sqlite3 /tmp/molecular_geometry.db < sql/molecular_geometry_schema.sql
sqlite3 /tmp/molecular_geometry.db < sql/sample_queries.sql

## Notebook

Open notebooks/molecular_geometry_workflow.ipynb in JupyterLab or VS Code.
