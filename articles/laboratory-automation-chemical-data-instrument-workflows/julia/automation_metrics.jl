#!/usr/bin/env julia

# Laboratory automation throughput and completion metrics using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
run_path = joinpath(base_dir, "data", "run_manifest.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(run_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

run_col = colindex("run_id")
instrument_col = colindex("instrument_id")
completed_col = colindex("completed_time")
qc_col = colindex("qc_status")

scheduled_count = size(raw, 1)
completed_count = count(!=("") , string.(raw[:, completed_col]))
failed_count = count(==("failed"), string.(raw[:, qc_col]))
warning_count = count(==("warning"), string.(raw[:, qc_col]))

completion_fraction = completed_count / scheduled_count
failure_fraction = failed_count / scheduled_count

rows = String["metric,value"]
push!(rows, string("scheduled_count,", scheduled_count))
push!(rows, string("completed_count,", completed_count))
push!(rows, string("failed_count,", failed_count))
push!(rows, string("warning_count,", warning_count))
push!(rows, string("completion_fraction,", completion_fraction))
push!(rows, string("failure_fraction,", failure_fraction))

open(joinpath(table_dir, "julia_automation_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_automation_metrics_report.md"), "w") do io
    println(io, "# Julia Laboratory Automation Metrics Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Completion fraction: ", completion_fraction)
    println(io, "Failure fraction: ", failure_fraction)
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia automation metrics complete.")
