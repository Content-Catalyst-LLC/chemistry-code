# Soil chemistry educational calculations in Julia.
# Includes soil organic carbon stock, base saturation, and nutrient balance.

using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

function soc_stock_mg_ha(soc_percent, bulk_density_g_cm3, depth_cm)
    return soc_percent * bulk_density_g_cm3 * depth_cm
end

function base_saturation_percent(base_cations_cmolc_kg, cec_cmolc_kg)
    return 100.0 * base_cations_cmolc_kg / cec_cmolc_kg
end

function nitrogen_balance(inputs, outputs)
    return sum(inputs) - sum(outputs)
end

soil_cases = [
    ("Field-A", 1.8, 1.32, 30.0, 8.4, 12.0),
    ("Wetland-C", 7.5, 0.82, 30.0, 28.0, 36.0),
    ("Pasture-E", 4.1, 1.05, 30.0, 18.2, 24.0)
]

open(joinpath(table_dir, "julia_soil_carbon_base_saturation.csv"), "w") do io
    println(io, "site,soc_percent,bulk_density_g_cm3,depth_cm,soc_stock_Mg_ha,base_saturation_percent")
    for (site, soc, bd, depth, bases, cec) in soil_cases
        println(io, "$(site),$(soc),$(bd),$(depth),$(soc_stock_mg_ha(soc, bd, depth)),$(base_saturation_percent(bases, cec))")
    end
end

field_b_balance = nitrogen_balance(
    [165.0, 35.0, 20.0],
    [145.0, 28.0, 22.0]
)

@printf("Field-B net nitrogen balance: %.2f kg/ha\n", field_b_balance)
println("Julia soil chemistry workflow complete.")
