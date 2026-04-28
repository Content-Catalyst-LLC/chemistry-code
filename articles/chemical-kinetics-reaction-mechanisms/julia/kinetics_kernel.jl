# Chemical kinetics numerical kernel in Julia.

function first_order_concentration(c0, k, t)
    return c0 * exp(-k * t)
end

function half_life_first_order(k)
    return log(2.0) / k
end

function arrhenius_rate_constant(A, Ea_j_mol, R, T)
    return A * exp(-Ea_j_mol / (R * T))
end

const R = 8.314462618

c20 = first_order_concentration(1.0, 0.15, 20.0)
t_half = half_life_first_order(0.15)
k310 = arrhenius_rate_constant(1.0e7, 55000.0, R, 310.0)

println("first_order_concentration_t20=", round(c20, digits=6))
println("first_order_half_life=", round(t_half, digits=6))
println("arrhenius_k_310K=", round(k310, digits=6))
