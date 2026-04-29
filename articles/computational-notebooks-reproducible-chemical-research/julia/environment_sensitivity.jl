#!/usr/bin/env julia

# Synthetic chemical notebook environment-sensitivity workflow.
# Uses Julia standard libraries only.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(base_dir, "data", "synthetic_chemical_notebook_runs.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(data_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

notebook_col = colindex("notebook_id")
env_col = colindex("environment_id")
abs_col = colindex("absorbance")

notebooks = unique(raw[:, notebook_col])
rows = String["notebook_id,environment_id,mean_absorbance,sd_absorbance,n"]

for notebook in notebooks
    mask = raw[:, notebook_col] .== notebook
    subset = raw[mask, :]
    envs = unique(subset[:, env_col])
    absorbance = parse.(Float64, string.(subset[:, abs_col]))

    push!(
        rows,
        string(
            notebook, ",",
            join(envs, ";"), ",",
            mean(absorbance), ",",
            std(absorbance), ",",
            length(absorbance)
        )
    )
end

open(joinpath(table_dir, "julia_environment_summary.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_environment_report.md"), "w") do io
    println(io, "# Julia Environment-Sensitivity Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "This report summarizes synthetic chemical notebook records by notebook and computational environment.")
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia environment-sensitivity workflow complete.")
