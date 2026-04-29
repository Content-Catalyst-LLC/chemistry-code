#!/usr/bin/env julia

# Polymer molar-mass and dispersity calculations using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
fractions_path = joinpath(base_dir, "data", "molar_mass_fractions.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(fractions_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

polymer_col = colindex("polymer_id")
count_col = colindex("molecule_count")
mass_col = colindex("molar_mass_g_mol")

polymer_ids = unique(string.(raw[:, polymer_col]))

rows = String["polymer_id,Mn_g_mol,Mw_g_mol,dispersity"]

for polymer_id in polymer_ids
    idx = findall(x -> string(x) == polymer_id, raw[:, polymer_col])
    counts = parse.(Float64, string.(raw[idx, count_col]))
    masses = parse.(Float64, string.(raw[idx, mass_col]))

    Mn = sum(counts .* masses) / sum(counts)
    Mw = sum(counts .* masses .* masses) / sum(counts .* masses)
    dispersity = Mw / Mn

    push!(rows, string(polymer_id, ",", Mn, ",", Mw, ",", dispersity))
end

open(joinpath(table_dir, "julia_polymer_molar_mass_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_polymer_molar_mass_report.md"), "w") do io
    println(io, "# Julia Polymer Molar-Mass Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Synthetic educational molar-mass and dispersity calculations.")
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia polymer molar-mass metrics complete.")
