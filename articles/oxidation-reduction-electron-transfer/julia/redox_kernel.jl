# Redox numerical kernel in Julia.

const R = 8.314462618
const F = 96485.33212

function cell_potential(e_cathode, e_anode)
    return e_cathode - e_anode
end

function delta_g(n, e_cell)
    return -n * F * e_cell / 1000.0
end

function nernst(e0, n, q, t)
    return e0 - (R * t / (n * F)) * log(q)
end

Ecell = cell_potential(0.34, -0.76)
DG = delta_g(2, Ecell)
E_nonstandard = nernst(1.10, 2, 100.0, 298.15)

println("E_cell_standard_V=", round(Ecell, digits=6))
println("delta_g_standard_kj_mol=", round(DG, digits=6))
println("E_nonstandard_V=", round(E_nonstandard, digits=6))
