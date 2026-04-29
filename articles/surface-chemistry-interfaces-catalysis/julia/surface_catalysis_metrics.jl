#!/usr/bin/env julia

# Surface coverage and rate-proxy calculations using Julia standard libraries.

using DelimitedFiles
using Statistics
using Dates

base_dir = normpath(joinpath(@__DIR__, ".."))
catalyst_path = joinpath(base_dir, "data", "catalyst_candidates.csv")
table_dir = joinpath(base_dir, "outputs", "tables")
report_dir = joinpath(base_dir, "outputs", "reports")

mkpath(table_dir)
mkpath(report_dir)

raw, header = readdlm(catalyst_path, ',', header=true)
columns = vec(header)

function colindex(name)
    idx = findfirst(==(name), columns)
    idx === nothing && error("Missing column: $name")
    return idx
end

id_col = colindex("catalyst_id")
ka_col = colindex("K_A_bar_inv")
kb_col = colindex("K_B_bar_inv")
ea_col = colindex("activation_energy_kJ_mol")
site_col = colindex("site_density_umol_g")

P_A = 1.0
P_B = 0.5
T = 550.0
R = 0.008314
A_pre = 1.0e5

rows = String["catalyst_id,theta_A,theta_B,rate_proxy"]

rate_values = Float64[]

for i in 1:size(raw, 1)
    catalyst_id = string(raw[i, id_col])
    K_A = parse(Float64, string(raw[i, ka_col]))
    K_B = parse(Float64, string(raw[i, kb_col]))
    E_a = parse(Float64, string(raw[i, ea_col]))
    sites = parse(Float64, string(raw[i, site_col]))

    denominator = 1.0 + K_A * P_A + K_B * P_B
    theta_A = K_A * P_A / denominator
    theta_B = K_B * P_B / denominator
    k = A_pre * exp(-E_a / (R * T))
    rate_proxy = k * theta_A * theta_B * sites

    push!(rate_values, rate_proxy)
    push!(rows, string(catalyst_id, ",", theta_A, ",", theta_B, ",", rate_proxy))
end

open(joinpath(table_dir, "julia_surface_catalysis_metrics.csv"), "w") do io
    println(io, join(rows, "\n"))
end

open(joinpath(report_dir, "julia_surface_catalysis_report.md"), "w") do io
    println(io, "# Julia Surface Catalysis Report")
    println(io)
    println(io, "Generated: ", Dates.now())
    println(io)
    println(io, "Mean synthetic rate proxy: ", mean(rate_values))
    println(io, "Maximum synthetic rate proxy: ", maximum(rate_values))
    println(io)
    println(io, "Responsible-use note: synthetic educational data only.")
end

println("Julia surface catalysis metrics complete.")
