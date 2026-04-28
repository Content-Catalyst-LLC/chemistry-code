# Intermolecular forces numerical kernel in Julia.

function lennard_jones(r_angstrom, epsilon_kj_mol, sigma_angstrom)
    ratio = sigma_angstrom / r_angstrom
    return 4.0 * epsilon_kj_mol * (ratio^12 - ratio^6)
end

function coulomb_relative(q1, q2, r)
    return q1 * q2 / r
end

epsilon = 0.997
sigma = 3.40
r_min = 2.0^(1.0 / 6.0) * sigma
u_min = lennard_jones(r_min, epsilon, sigma)

println("r_min_angstrom=", round(r_min, digits=6))
println("u_min_kj_mol=", round(u_min, digits=6))
println("relative_coulomb_attraction=", round(coulomb_relative(1.0, -1.0, 2.0), digits=6))
