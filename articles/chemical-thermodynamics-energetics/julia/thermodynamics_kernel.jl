# Chemical thermodynamics numerical kernel in Julia.

const R = 8.314462618

function gibbs_free_energy(delta_h_kj_mol, delta_s_j_mol_k, temperature_k)
    return delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0
end

function equilibrium_constant(delta_g_standard_kj_mol, temperature_k)
    return exp(-(delta_g_standard_kj_mol * 1000.0) / (R * temperature_k))
end

function calorimetry_delta_h(mass_g, specific_heat_j_g_k, delta_t_k, amount_mol)
    q_solution_j = mass_g * specific_heat_j_g_k * delta_t_k
    q_reaction_j = -q_solution_j
    return q_reaction_j / 1000.0 / amount_mol
end

dg = gibbs_free_energy(-80.0, -100.0, 298.15)
k = equilibrium_constant(dg, 298.15)
dh_cal = calorimetry_delta_h(100.0, 4.184, 6.2, 0.0500)

println("delta_g_kj_mol=", round(dg, digits=6))
println("equilibrium_constant=", round(k, digits=6))
println("calorimetry_delta_h_kj_mol=", round(dh_cal, digits=6))
