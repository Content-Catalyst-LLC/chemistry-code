# Reaction-network numerical kernel in Julia.

function simulate_network(k1, k2, k3, k4, dt, total_time)
    A = 1.0
    B = 0.0
    C = 0.0
    D = 0.0
    E = 0.0

    for t in 0:dt:total_time
        r1 = k1 * A
        r2 = k2 * B
        r3 = k3 * A
        r4 = k4 * B

        A = max(A + (-r1 - r3) * dt, 0.0)
        B = max(B + (r1 - r2 - r4) * dt, 0.0)
        C = max(C + r2 * dt, 0.0)
        D = max(D + r3 * dt, 0.0)
        E = max(E + r4 * dt, 0.0)
    end

    return A, B, C, D, E
end

A, B, C, D, E = simulate_network(0.20, 0.08, 0.05, 0.03, 0.25, 50.0)

println("A_final=", round(A, digits=6))
println("B_final=", round(B, digits=6))
println("C_final=", round(C, digits=6))
println("D_final=", round(D, digits=6))
println("E_final=", round(E, digits=6))
