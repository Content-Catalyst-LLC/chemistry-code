# Stoichiometry numerical kernel in Julia.

function limiting_extent(available_moles, coefficients)
    return minimum(available_moles ./ coefficients)
end

function percent_yield(actual_yield, theoretical_yield)
    return actual_yield / theoretical_yield * 100.0
end

function dilution_volume(c1, c2, v2)
    return (c2 * v2) / c1
end

available = [4.0, 1.5]
coefficients = [2.0, 1.0]
extent = limiting_extent(available, coefficients)
water_moles = extent * 2.0
theoretical_yield = water_moles * 18.01528

println("maximum_extent_mol=", round(extent, digits=6))
println("water_moles_theoretical=", round(water_moles, digits=6))
println("theoretical_yield_g=", round(theoretical_yield, digits=6))
println("percent_yield=", round(percent_yield(45.0, theoretical_yield), digits=6))
println("stock_volume_L=", round(dilution_volume(1.0, 0.1, 0.25), digits=6))
