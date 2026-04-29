# Computational chemistry numerical kernel in Julia.

const R = 8.314462618
const kB = 1.380649e-23
const h = 6.62607015e-34

function boltzmann_weight(delta_e_kj_mol, temperature_k)
    return exp(-(delta_e_kj_mol * 1000.0) / (R * temperature_k))
end

function lennard_jones(r, epsilon, sigma)
    ratio = sigma / r
    return 4.0 * epsilon * (ratio^12 - ratio^6)
end

function tanimoto(a, b, c)
    return c / (a + b - c)
end

function tst_rate(delta_g_dagger_kj_mol, temperature_k)
    return (kB * temperature_k / h) * exp(-(delta_g_dagger_kj_mol * 1000.0) / (R * temperature_k))
end

println("boltzmann_weight=", round(boltzmann_weight(2.5, 298.15), digits=6))
println("lennard_jones=", round(lennard_jones(1.12, 1.0, 1.0), digits=6))
println("tanimoto=", round(tanimoto(5.0, 4.0, 3.0), digits=6))
println("tst_rate=", tst_rate(55.0, 298.15))
