# Inorganic chemistry numerical kernel in Julia.

function oxidation_state(total_charge, known_contribution, unknown_atom_count)
    return (total_charge - known_contribution) / unknown_atom_count
end

function cfse(t2g_electrons, eg_electrons, delta_o)
    return t2g_electrons * (-0.4 * delta_o) + eg_electrons * (0.6 * delta_o)
end

function spin_only_moment(unpaired_electrons)
    return sqrt(unpaired_electrons * (unpaired_electrons + 2.0))
end

function tolerance_factor(rA, rB, rX)
    return (rA + rX) / (sqrt(2.0) * (rB + rX))
end

println("Mn_in_KMnO4_OS=", round(oxidation_state(0.0, -7.0, 1.0), digits=6))
println("octahedral_d3_CFSE=", round(cfse(3.0, 0.0, 1.0), digits=6))
println("spin_only_d3=", round(spin_only_moment(3.0), digits=6))
println("tolerance_factor=", round(tolerance_factor(1.60, 0.60, 1.40), digits=6))
