# Introductory chemistry numerical kernel in Julia.

function moles_from_mass(mass_g, molar_mass_g_mol)
    return mass_g / molar_mass_g_mol
end

function molarity(moles, volume_l)
    return moles / volume_l
end

function first_order_concentration(initial_concentration, rate_constant, time)
    return initial_concentration * exp(-rate_constant * time)
end

n = moles_from_mass(5.844, 58.44)
c = molarity(n, 0.500)
a_t = first_order_concentration(1.0, 0.15, 10.0)

println("moles=", round(n, digits=5))
println("molarity_mol_l=", round(c, digits=5))
println("first_order_concentration=", round(a_t, digits=5))
