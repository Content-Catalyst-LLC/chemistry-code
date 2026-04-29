# Molecular dynamics numerical kernel in Julia.

function lennard_jones(r, epsilon, sigma)
    ratio = sigma / r
    return 4.0 * epsilon * (ratio^12 - ratio^6)
end

function velocity_verlet_position(r, v, a, dt)
    return r + v * dt + 0.5 * a * dt^2
end

function velocity_update(v, a, dt)
    return v + a * dt
end

function diffusion_from_msd(msd, t)
    return msd / (6.0 * t)
end

r_new = velocity_verlet_position(0.0, 0.05, 0.10, 0.5)
v_new = velocity_update(0.05, 0.10, 0.5)

println("new_position=", round(r_new, digits=6))
println("new_velocity=", round(v_new, digits=6))
println("lj_energy=", round(lennard_jones(1.12, 1.0, 1.0), digits=6))
println("diffusion_estimate=", round(diffusion_from_msd(4.21, 7.0), digits=6))
