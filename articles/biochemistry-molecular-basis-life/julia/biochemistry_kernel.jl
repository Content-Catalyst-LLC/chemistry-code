# Biochemistry numerical kernel in Julia.

function michaelis_menten(substrate, vmax, km)
    return vmax * substrate / (km + substrate)
end

function occupancy(ligand, kd)
    return ligand / (kd + ligand)
end

function hill_occupancy(ligand, kd, n)
    return ligand^n / (kd^n + ligand^n)
end

function delta_g_standard(K, T)
    R = 8.314462618
    return -(R * T * log(K)) / 1000.0
end

println("velocity=", round(michaelis_menten(5.0, 120.0, 3.5), digits=6))
println("occupancy=", round(occupancy(2.0, 2.0), digits=6))
println("hill_occupancy=", round(hill_occupancy(2.0, 2.0, 2.0), digits=6))
println("delta_g_kj_mol=", round(delta_g_standard(1000.0, 298.15), digits=6))
