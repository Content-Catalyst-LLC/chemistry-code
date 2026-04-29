# Atmospheric chemistry educational calculations in Julia.
# Includes CO2 forcing approximation, first-order lifetime, and a simplified
# photochemical ozone production index.

using DelimitedFiles
using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

function co2_forcing(current_ppm, reference_ppm)
    return 5.35 * log(current_ppm / reference_ppm)
end

function first_order_concentration(c0, k, t)
    return c0 * exp(-k * t)
end

function ozone_production_index(nox_ppb, voc_ppb, sunlight_index)
    return sunlight_index * sqrt(max(nox_ppb, 0.0) * max(voc_ppb, 0.0))
end

forcing = co2_forcing(423.0, 280.0)
@printf("Approximate CO2 forcing: %.3f W/m2\n", forcing)

rows = [["day" "mixing_ratio_ppb" "fraction_remaining"]]
c0 = 100.0
k = 0.20

for day in 0:2:30
    c = first_order_concentration(c0, k, day)
    rows = vcat(rows, [day c c / c0])
end

open(joinpath(table_dir, "julia_atmospheric_decay.csv"), "w") do io
    for row in eachrow(rows)
        println(io, join(row, ","))
    end
end

ozone_rows = [
    "case,nox_ppb,voc_ppb,sunlight_index,ozone_production_index",
    "low_NOx_low_VOC,5.0,20.0,0.8,$(ozone_production_index(5.0, 20.0, 0.8))",
    "urban_sunny,35.0,80.0,1.0,$(ozone_production_index(35.0, 80.0, 1.0))",
    "biogenic_hot_sunny,12.0,140.0,1.2,$(ozone_production_index(12.0, 140.0, 1.2))"
]

open(joinpath(table_dir, "julia_ozone_index.csv"), "w") do io
    for line in ozone_rows
        println(io, line)
    end
end

println("Julia atmospheric chemistry workflow complete.")
