#!/usr/bin/env julia

# Electronic and photochemical materials metrics using Julia standard libraries.

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
edge_col = colindex("absorption_edge_nm")
electron_col = colindex("electron_mobility_cm2_V_s")
hole_col = colindex("hole_mobility_cm2_V_s")
lifetime_col = colindex("carrier_lifetime_ns")

rows = String["material_id,edge_band_gap_estimate_eV,mobility_balance_ratio,transport_proxy"]
transport_values = Float64[]

for i in 1:size(raw, 1)
    material_id = string(raw[i, id_col])
    edge_nm = parse(Float64, string(raw[i, edge_col]))
    electron_mobility = parse(Float64, string(raw[i, electron_col]))
    hole_mobility = parse(Float64, string(raw[i, hole_col]))
    lifetime = parse(Float64, string(raw[i, lifetime_col]))

    edge_band_gap = 1240.0 / edge_nm
    mobility_balance = min(electron_mobility, hole_mobility) / max(electron_mobility, hole_mobility)
    transport_proxy = (electron_mobility + hole_mobility) * lifetime

    push!(transport_values, transport_proxy)
    push!(rows, string(material_id, ",", edge_band_gap, ",", mobility_balance, ",", transport_proxy))
end

open(joinpath(table_dir, "julia_electronic_photochemical_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_electronic_photochemical_metrics_report.md"), "w") do io
    println(io, "# Julia Electronic and Photochemical Materials Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean synthetic transport proxy: ", mean(transport_values))
    println(io, "Maximum synthetic transport proxy: ", maximum(transport_values))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia electronic and photochemical metrics complete.")
