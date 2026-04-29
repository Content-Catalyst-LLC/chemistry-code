#!/usr/bin/env julia

# Electrochemical capacity and energy metrics using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
cells_path = joinpath(base_dir, "data", "cell_candidates.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(cells_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

id_col = colindex("cell_id")
voltage_col = colindex("nominal_voltage_V")
capacity_col = colindex("specific_capacity_mAh_g")
mass_col = colindex("active_material_mass_g")
retention_col = colindex("cycle_100_capacity_retention")
ce_col = colindex("coulombic_efficiency")

rows = String["cell_id,cell_capacity_mAh,cell_energy_Wh,cycle_loss_percent,coulombic_efficiency"]
energy_values = Float64[]

for i in 1:size(raw, 1)
    cell_id = string(raw[i, id_col])
    voltage = parse(Float64, string(raw[i, voltage_col]))
    specific_capacity = parse(Float64, string(raw[i, capacity_col]))
    active_mass = parse(Float64, string(raw[i, mass_col]))
    retention = parse(Float64, string(raw[i, retention_col]))
    ce = parse(Float64, string(raw[i, ce_col]))

    cell_capacity = specific_capacity * active_mass
    cell_energy = cell_capacity * voltage / 1000.0
    cycle_loss_percent = 100.0 * (1.0 - retention)

    push!(energy_values, cell_energy)
    push!(rows, string(cell_id, ",", cell_capacity, ",", cell_energy, ",", cycle_loss_percent, ",", ce))
end

open(joinpath(table_dir, "julia_electrochemistry_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_electrochemistry_metrics_report.md"), "w") do io
    println(io, "# Julia Electrochemistry Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean synthetic cell energy Wh: ", mean(energy_values))
    println(io, "Maximum synthetic cell energy Wh: ", maximum(energy_values))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia electrochemistry metrics complete.")
