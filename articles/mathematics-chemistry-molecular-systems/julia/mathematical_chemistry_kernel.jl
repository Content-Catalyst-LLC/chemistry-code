# Mathematical chemistry numerical kernel in Julia.

function first_order_concentration(initial_concentration, rate_constant, time)
    return initial_concentration * exp(-rate_constant * time)
end

function equilibrium_constant(delta_g_standard_kj_mol, temperature_k)
    R = 8.314462618
    return exp(-(delta_g_standard_kj_mol * 1000.0) / (R * temperature_k))
end

function distance(point_a, point_b)
    return sqrt(sum((point_a .- point_b).^2))
end

c10 = first_order_concentration(1.0, 0.15, 10.0)
k_eq = equilibrium_constant(-5.0, 298.15)
d_oh = distance([0.0, 0.0, 0.0], [0.958, 0.0, 0.0])

println("first_order_concentration_t10=", round(c10, digits=6))
println("equilibrium_constant=", round(k_eq, digits=6))
println("distance_oh_angstrom=", round(d_oh, digits=6))
