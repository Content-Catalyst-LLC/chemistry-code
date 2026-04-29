#!/usr/bin/env julia

# Retention-factor and resolution calculations using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
data_path = joinpath(base_dir, "data", "chromatographic_peaks.csv")
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

peak_col = colindex("peak_id")
sample_col = colindex("sample_id")
rt_col = colindex("retention_time_min")
width_col = colindex("baseline_width_min")

dead_time = 0.92
rows = String["peak_id,sample_id,retention_time_min,baseline_width_min,retention_factor_k"]

for i in 1:size(raw, 1)
    peak_id = string(raw[i, peak_col])
    sample_id = string(raw[i, sample_col])
    retention_time = parse(Float64, string(raw[i, rt_col]))
    width = parse(Float64, string(raw[i, width_col]))
    k = (retention_time - dead_time) / dead_time
    push!(rows, string(peak_id, ",", sample_id, ",", retention_time, ",", width, ",", k))
end

open(joinpath(table_dir, "julia_retention_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_chromatography_metrics_report.md"), "w") do io
    println(io, "# Julia Chromatography Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    retention_times = parse.(Float64, string.(raw[:, rt_col]))
    println(io, "Mean retention time: ", mean(retention_times))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia chromatography metrics complete.")
