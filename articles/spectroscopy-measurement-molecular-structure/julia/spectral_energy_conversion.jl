#!/usr/bin/env julia

# Spectral energy conversion workflow using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(base_dir, "data", "ir_peaks.csv")
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

wavenumber_col = colindex("wavenumber_cm_minus_1")
sample_col = colindex("sample_id")

h = 6.62607015e-34
c = 299792458.0
na = 6.02214076e23

rows = String["sample_id,wavenumber_cm_minus_1,photon_energy_kj_mol"]

for i in 1:size(raw, 1)
    sample_id = string(raw[i, sample_col])
    wavenumber = parse(Float64, string(raw[i, wavenumber_col]))
    energy_kj_mol = h * c * wavenumber * 100.0 * na / 1000.0
    push!(rows, string(sample_id, ",", wavenumber, ",", energy_kj_mol))
end

open(joinpath(table_dir, "julia_spectral_energy_conversion.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_spectral_energy_report.md"), "w") do io
    println(io, "# Julia Spectral Energy Conversion Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean IR wavenumber: ", mean(parse.(Float64, string.(raw[:, wavenumber_col]))))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia spectral energy conversion complete.")
