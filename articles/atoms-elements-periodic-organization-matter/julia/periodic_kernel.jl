# Periodic organization numerical kernel in Julia.

const AVOGADRO_CONSTANT = 6.02214076e23

function neutron_number(mass_number, atomic_number)
    return mass_number - atomic_number
end

function isotope_weighted_mass(masses, abundances)
    return sum(masses .* abundances)
end

function amount_from_mass(mass_g, molar_mass_g_mol)
    return mass_g / molar_mass_g_mol
end

cl_mass = isotope_weighted_mass([34.96885268, 36.96590260], [0.7576, 0.2424])
c14_neutrons = neutron_number(14, 6)
water_moles = amount_from_mass(18.015, 18.015)
water_entities = water_moles * AVOGADRO_CONSTANT

println("chlorine_weighted_atomic_mass_u=", round(cl_mass, digits=6))
println("carbon_14_neutron_number=", c14_neutrons)
println("water_amount_mol=", round(water_moles, digits=6))
println("water_estimated_entities=", water_entities)
