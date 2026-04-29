# Physical chemistry numerical kernel in Julia.

const R = 8.314462618
const F = 96485.33212
const kB = 1.380649e-23

function equilibrium_constant(delta_g_kj_mol, temperature_k)
    return exp(-(delta_g_kj_mol * 1000.0) / (R * temperature_k))
end

function arrhenius(A, Ea_kj_mol, temperature_k)
    return A * exp(-(Ea_kj_mol * 1000.0) / (R * temperature_k))
end

function nernst(E0, n, Q, T)
    return E0 - (R * T / (n * F)) * log(Q)
end

println("K_demo=", round(equilibrium_constant(-20.0, 298.15), digits=6))
println("k_demo=", arrhenius(1.0e12, 75.0, 298.15))
println("E_demo=", round(nernst(1.10, 2.0, 100.0, 298.15), digits=6))
