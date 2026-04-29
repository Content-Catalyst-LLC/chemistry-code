#!/usr/bin/env julia

# Materials objective-function calculations using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
materials_path = joinpath(base_dir, "data", "material_candidates.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(materials_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

id_col = colindex("material_id")
density_col = colindex("density_g_cm3")
modulus_col = colindex("modulus_GPa")
thermal_col = colindex("thermal_stability_C")
recycle_col = colindex("recyclability_score")
cost_col = colindex("relative_cost_score")

target_density = 1.5
target_modulus = 10.0
target_thermal = 300.0
target_recycle = 0.85
target_cost = 0.30

rows = String["material_id,objective_score"]

scores = Float64[]

for i in 1:size(raw, 1)
    material_id = string(raw[i, id_col])
    density = parse(Float64, string(raw[i, density_col]))
    modulus = parse(Float64, string(raw[i, modulus_col]))
    thermal = parse(Float64, string(raw[i, thermal_col]))
    recycle = parse(Float64, string(raw[i, recycle_col]))
    cost = parse(Float64, string(raw[i, cost_col]))

    score =
        1.2 * ((density - target_density) / 1.0)^2 +
        0.8 * ((modulus - target_modulus) / 25.0)^2 +
        1.0 * ((thermal - target_thermal) / 250.0)^2 +
        1.4 * ((recycle - target_recycle) / 0.25)^2 +
        1.2 * ((cost - target_cost) / 0.30)^2

    push!(scores, score)
    push!(rows, string(material_id, ",", score))
end

open(joinpath(table_dir, "julia_materials_objective_scores.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_materials_objective_report.md"), "w") do io
    println(io, "# Julia Materials Objective Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean objective score: ", mean(scores))
    println(io, "Minimum objective score: ", minimum(scores))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia materials objective metrics complete.")
