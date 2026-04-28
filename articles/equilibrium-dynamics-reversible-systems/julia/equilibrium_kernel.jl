# Chemical equilibrium numerical kernel in Julia.

const R = 8.314462618

function delta_g_from_qk(Q, K, T)
    return R * T * log(Q / K) / 1000.0
end

function solve_isomerization(K, total)
    Aeq = total / (1.0 + K)
    Beq = total - Aeq
    return Aeq, Beq
end

function reversible_step(A, B, kf, kr, dt)
    net = kf * A - kr * B
    return max(A - net * dt, 0.0), max(B + net * dt, 0.0)
end

Aeq, Beq = solve_isomerization(4.0, 1.0)
dg = delta_g_from_qk(0.5, 4.0, 298.15)
A1, B1 = reversible_step(1.0, 0.0, 0.20, 0.05, 0.25)

println("A_eq=", round(Aeq, digits=6))
println("B_eq=", round(Beq, digits=6))
println("delta_g_kj_mol=", round(dg, digits=6))
println("A_after_step=", round(A1, digits=6))
println("B_after_step=", round(B1, digits=6))
