# Organic-structure numerical kernel in Julia.

function dbe(C, H, N, X)
    return C - (H + X) / 2.0 + N / 2.0 + 1.0
end

function polarity_score(heteroatoms, donors, acceptors)
    return heteroatoms + donors + acceptors
end

function boltzmann_populations(energies_kj_mol, temperature_k)
    R = 0.008314462618
    weights = exp.(-energies_kj_mol ./ (R * temperature_k))
    return weights ./ sum(weights)
end

println("benzene_DBE=", round(dbe(6, 6, 0, 0), digits=6))
println("acetic_acid_DBE=", round(dbe(2, 4, 0, 0), digits=6))
println("polarity_score=", polarity_score(2, 1, 2))
println("conformer_populations=", round.(boltzmann_populations([0.0, 2.5, 6.0], 298.15), digits=6))
