# Quantum chemistry numerical kernel in Julia.

const R = 8.314462618
const kB = 1.380649e-23
const h = 6.62607015e-34

function boltzmann_weight(delta_e_kj_mol, temperature_k)
    return exp(-(delta_e_kj_mol * 1000.0) / (R * temperature_k))
end

function tst_rate(delta_g_dagger_kj_mol, temperature_k)
    return (kB * temperature_k / h) * exp(-(delta_g_dagger_kj_mol * 1000.0) / (R * temperature_k))
end

function two_level_energies(ea, eb, v)
    trace = ea + eb
    diff = ea - eb
    split = sqrt(diff^2 + 4.0 * v^2)
    return ((trace - split) / 2.0, (trace + split) / 2.0)
end

e1, e2 = two_level_energies(-10.0, -8.0, -2.0)

println("two_level_E1=", round(e1, digits=6))
println("two_level_E2=", round(e2, digits=6))
println("boltzmann_weight=", round(boltzmann_weight(25.0, 298.15), digits=10))
println("tst_rate=", tst_rate(50.0, 298.15))
