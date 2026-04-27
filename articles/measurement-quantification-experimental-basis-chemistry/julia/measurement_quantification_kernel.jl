# Measurement and quantification numerical kernel in Julia.

function moles_from_mass(mass_g, molar_mass_g_mol)
    return mass_g / molar_mass_g_mol
end

function concentration_mol_l(moles, volume_l)
    return moles / volume_l
end

function dilution_stock_volume(c1, c2, v2)
    return (c2 * v2) / c1
end

n = moles_from_mass(5.844, 58.44)
c = concentration_mol_l(n, 0.500)
v1 = dilution_stock_volume(1.0, 0.10, 100.0)

println("moles=", round(n, digits=6))
println("concentration_mol_l=", round(c, digits=6))
println("stock_volume_ml=", round(v1, digits=6))
