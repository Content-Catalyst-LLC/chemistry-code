#!/usr/bin/env julia

# Mass-error and isotope-spacing calculations using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
features_path = joinpath(base_dir, "data", "ms_features.csv")
candidates_path = joinpath(base_dir, "data", "candidate_library.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

features, fheader = readdlm(features_path, ',', header=true)
candidates, cheader = readdlm(candidates_path, ',', header=true)

fcols = vec(fheader)
ccols = vec(cheader)

function colindex(cols, name)
    idx = findfirst(==(name), cols)
    idx === nothing && error("Missing column: $name")
    return idx
end

feature_id_col = colindex(fcols, "feature_id")
observed_col = colindex(fcols, "observed_mz")
charge_col = colindex(fcols, "charge")

candidate_name_col = colindex(ccols, "candidate_name")
theoretical_col = colindex(ccols, "theoretical_mz")
expected_charge_col = colindex(ccols, "expected_charge")

rows = String["feature_id,candidate_name,observed_mz,theoretical_mz,ppm_error,charge"]

for i in 1:size(features, 1)
    feature_id = string(features[i, feature_id_col])
    observed = parse(Float64, string(features[i, observed_col]))
    charge = parse(Int, string(features[i, charge_col]))

    for j in 1:size(candidates, 1)
        candidate_name = string(candidates[j, candidate_name_col])
        theoretical = parse(Float64, string(candidates[j, theoretical_col]))
        expected_charge = parse(Int, string(candidates[j, expected_charge_col]))

        if charge == expected_charge
            ppm = (observed - theoretical) / theoretical * 1_000_000.0
            if abs(ppm) <= 5.0
                push!(rows, string(feature_id, ",", candidate_name, ",", observed, ",", theoretical, ",", ppm, ",", charge))
            end
        end
    end
end

open(joinpath(table_dir, "julia_mass_error_matches.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_mass_error_report.md"), "w") do io
    println(io, "# Julia Mass Error Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    observed_values = parse.(Float64, string.(features[:, observed_col]))
    println(io, "Mean observed m/z: ", mean(observed_values))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia mass-error workflow complete.")
