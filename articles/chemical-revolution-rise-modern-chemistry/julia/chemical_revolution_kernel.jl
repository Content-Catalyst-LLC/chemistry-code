# Chemical Revolution numerical kernel in Julia.

function oxide_mass(metal_mass_g, oxygen_mass_g)
    return metal_mass_g + oxygen_mass_g
end

function oxygen_mass_fraction(metal_mass_g, oxygen_mass_g)
    return oxygen_mass_g / oxide_mass(metal_mass_g, oxygen_mass_g)
end

function mass_difference(reactant_mass_g, product_mass_g)
    return product_mass_g - reactant_mass_g
end

println("magnesium_oxide_mass_g=", round(oxide_mass(24.305, 16.000), digits=5))
println("oxygen_mass_fraction=", round(oxygen_mass_fraction(24.305, 16.000), digits=5))
println("mass_difference_closed_system=", round(mass_difference(44.0, 44.0), digits=5))
