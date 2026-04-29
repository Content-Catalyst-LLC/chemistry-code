#!/usr/bin/env julia

# Electrochemical metric calculations using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
calibration_path = joinpath(base_dir, "data", "sensor_calibration.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(calibration_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

concentration_col = colindex("concentration_uM")
current_col = colindex("current_uA")

x = parse.(Float64, string.(raw[:, concentration_col]))
y = parse.(Float64, string.(raw[:, current_col]))

xbar = mean(x)
ybar = mean(y)
slope = sum((x .- xbar) .* (y .- ybar)) / sum((x .- xbar).^2)
intercept = ybar - slope * xbar

blank_currents = [y[i] for i in eachindex(y) if x[i] == 0.0]
blank_sd = std(blank_currents)
lod = 3.0 * blank_sd / slope

rows = String["metric,value"]
push!(rows, string("sensitivity_uA_per_uM,", slope))
push!(rows, string("intercept_uA,", intercept))
push!(rows, string("blank_sd_uA,", blank_sd))
push!(rows, string("limit_of_detection_uM,", lod))

open(joinpath(table_dir, "julia_electrochemical_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_electrochemical_metrics_report.md"), "w") do io
    println(io, "# Julia Electrochemical Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Sensitivity uA/uM: ", slope)
    println(io, "Estimated LOD uM: ", lod)
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia electrochemical metrics complete.")
