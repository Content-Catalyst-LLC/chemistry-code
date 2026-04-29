#!/usr/bin/env julia

# Industrial chemistry process metrics using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
routes_path = joinpath(base_dir, "data", "process_routes.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(routes_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

id_col = colindex("route_id")
theoretical_col = colindex("theoretical_product_kg")
actual_col = colindex("actual_product_kg")
waste_col = colindex("waste_kg")
solvent_col = colindex("solvent_kg")
energy_col = colindex("energy_kWh")
volume_col = colindex("reactor_volume_m3")
time_col = colindex("batch_or_residence_time_h")

rows = String["route_id,yield_fraction,e_factor,solvent_intensity,energy_intensity_kWh_kg,space_time_yield_kg_m3_h"]
e_factors = Float64[]

for i in 1:size(raw, 1)
    route_id = string(raw[i, id_col])
    theoretical = parse(Float64, string(raw[i, theoretical_col]))
    actual = parse(Float64, string(raw[i, actual_col]))
    waste = parse(Float64, string(raw[i, waste_col]))
    solvent = parse(Float64, string(raw[i, solvent_col]))
    energy = parse(Float64, string(raw[i, energy_col]))
    volume = parse(Float64, string(raw[i, volume_col]))
    time_h = parse(Float64, string(raw[i, time_col]))

    yield_fraction = actual / theoretical
    e_factor = waste / actual
    solvent_intensity = solvent / actual
    energy_intensity = energy / actual
    space_time_yield = actual / (volume * time_h)

    push!(e_factors, e_factor)
    push!(rows, string(route_id, ",", yield_fraction, ",", e_factor, ",", solvent_intensity, ",", energy_intensity, ",", space_time_yield))
end

open(joinpath(table_dir, "julia_industrial_process_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_industrial_process_metrics_report.md"), "w") do io
    println(io, "# Julia Industrial Process Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean synthetic E-factor: ", mean(e_factors))
    println(io, "Maximum synthetic E-factor: ", maximum(e_factors))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia industrial process metrics complete.")
