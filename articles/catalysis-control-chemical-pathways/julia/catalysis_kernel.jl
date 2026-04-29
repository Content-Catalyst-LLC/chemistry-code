# Catalysis numerical kernel in Julia.

const R = 8.314462618

function rate_enhancement(delta_ea_kj_mol, temperature_k)
    return exp((delta_ea_kj_mol * 1000.0) / (R * temperature_k))
end

function turnover_number(product_mol, catalyst_mol)
    return product_mol / catalyst_mol
end

function turnover_frequency(product_mol, catalyst_mol, time_s)
    return turnover_number(product_mol, catalyst_mol) / time_s
end

function langmuir_theta(K, P)
    return (K * P) / (1.0 + K * P)
end

println("rate_enhancement=", round(rate_enhancement(25.0, 298.15), digits=6))
println("TON=", round(turnover_number(0.05, 0.0005), digits=6))
println("TOF=", round(turnover_frequency(0.05, 0.0005, 3600.0), digits=8))
println("theta=", round(langmuir_theta(1.5, 1.0), digits=6))
