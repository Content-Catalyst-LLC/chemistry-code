# Chemical bonding numerical kernel in Julia.

function bond_order(bonding_electrons, antibonding_electrons)
    return (bonding_electrons - antibonding_electrons) / 2
end

function electronegativity_difference(chi_a, chi_b)
    return abs(chi_a - chi_b)
end

function distance(point_a, point_b)
    return sqrt(sum((point_a .- point_b).^2))
end

oh_distance = distance([0.0, 0.0, 0.0], [0.958, 0.0, 0.0])
oh_delta_chi = electronegativity_difference(3.44, 2.20)
h2_bond_order = bond_order(2, 0)

println("oh_distance_angstrom=", round(oh_distance, digits=6))
println("oh_delta_chi=", round(oh_delta_chi, digits=6))
println("h2_bond_order=", round(h2_bond_order, digits=6))
