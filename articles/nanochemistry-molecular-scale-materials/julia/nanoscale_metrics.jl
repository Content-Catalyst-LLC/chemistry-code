#!/usr/bin/env julia

# Nanoscale surface-area and diffusion metrics using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
candidate_path = joinpath(base_dir, "data", "nanomaterial_candidates.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(candidate_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

sample_col = colindex("sample_id")
core_col = colindex("core_diameter_nm")
hydro_col = colindex("hydrodynamic_diameter_nm")

kB = 1.380649e-23
T = 298.15
eta = 0.00089

rows = String["sample_id,surface_area_to_volume_nm_inv,diffusion_m2_s"]
diffusions = Float64[]

for i in 1:size(raw, 1)
    sample_id = string(raw[i, sample_col])
    core_diameter_nm = parse(Float64, string(raw[i, core_col]))
    hydrodynamic_diameter_nm = parse(Float64, string(raw[i, hydro_col]))

    surface_area_to_volume = 6.0 / core_diameter_nm
    diffusion = kB * T / (3.0 * pi * eta * hydrodynamic_diameter_nm * 1e-9)

    push!(diffusions, diffusion)
    push!(rows, string(sample_id, ",", surface_area_to_volume, ",", diffusion))
end

open(joinpath(table_dir, "julia_nanoscale_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_nanoscale_metrics_report.md"), "w") do io
    println(io, "# Julia Nanoscale Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean diffusion estimate: ", mean(diffusions))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia nanoscale metrics complete.")
