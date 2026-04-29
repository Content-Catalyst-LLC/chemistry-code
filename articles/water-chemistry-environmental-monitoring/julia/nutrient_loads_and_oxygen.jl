# Water chemistry educational calculations in Julia.
# Includes nutrient load, oxygen deficit, and simple pH flags.

using DelimitedFiles
using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

function nutrient_load_kg_day(concentration_mg_L, flow_L_s)
    return concentration_mg_L * flow_L_s * 0.0864
end

function oxygen_deficit(do_saturation_mg_L, observed_do_mg_L)
    return max(do_saturation_mg_L - observed_do_mg_L, 0.0)
end

function ph_flag(pH)
    if pH < 6.5 || pH > 9.0
        return "outside_illustrative_aquatic_range"
    else
        return "within_illustrative_aquatic_range"
    end
end

cases = [
    ("River-A nitrate", 7.8, 820.0),
    ("River-A phosphate", 0.18, 820.0),
    ("Reservoir-G phosphorus", 0.07, 140.0),
    ("Wetland-E ammonia", 0.62, 18.0)
]

open(joinpath(table_dir, "julia_nutrient_loads.csv"), "w") do io
    println(io, "case,concentration_mg_L,flow_L_s,load_kg_day")
    for (name, c, q) in cases
        println(io, "$(name),$(c),$(q),$(nutrient_load_kg_day(c, q))")
    end
end

oxygen_cases = [
    ("Lake-B", 8.7, 5.6),
    ("Reservoir-G", 8.3, 4.6),
    ("River-A", 10.2, 8.2)
]

open(joinpath(table_dir, "julia_oxygen_deficits.csv"), "w") do io
    println(io, "site,do_saturation_mg_L,observed_do_mg_L,oxygen_deficit_mg_L")
    for (site, sat, obs) in oxygen_cases
        println(io, "$(site),$(sat),$(obs),$(oxygen_deficit(sat, obs))")
    end
end

println("pH flags")
for (site, pH) in [("River-A", 7.4), ("Lake-B", 8.6), ("Mine-F", 5.2)]
    @printf("%s | pH %.2f | %s\n", site, pH, ph_flag(pH))
end

println("Julia water chemistry workflow complete.")
