#!/usr/bin/env julia

# Colloid diffusion and viscosity metrics using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
systems_path = joinpath(base_dir, "data", "colloid_systems.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(systems_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

id_col = colindex("formulation_id")
diameter_col = colindex("particle_or_droplet_size_nm")
phi_col = colindex("volume_fraction")

kB = 1.380649e-23
T = 298.15
eta0 = 0.00089

rows = String["formulation_id,diffusion_m2_s,einstein_relative_viscosity"]
diffusions = Float64[]

for i in 1:size(raw, 1)
    formulation_id = string(raw[i, id_col])
    diameter_nm = parse(Float64, string(raw[i, diameter_col]))
    phi = parse(Float64, string(raw[i, phi_col]))

    diffusion = kB * T / (3.0 * pi * eta0 * diameter_nm * 1e-9)
    einstein_relative_viscosity = 1.0 + 2.5 * phi

    push!(diffusions, diffusion)
    push!(rows, string(formulation_id, ",", diffusion, ",", einstein_relative_viscosity))
end

open(joinpath(table_dir, "julia_colloid_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_colloid_metrics_report.md"), "w") do io
    println(io, "# Julia Colloid Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean diffusion estimate: ", mean(diffusions))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia colloid metrics complete.")
