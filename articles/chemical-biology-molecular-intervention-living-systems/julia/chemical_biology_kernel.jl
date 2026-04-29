# Chemical biology numerical kernel in Julia.

function dose_response(concentration, ec50, hill, bottom, top)
    return bottom + (top - bottom) / (1.0 + (ec50 / concentration)^hill)
end

function occupancy(ligand, kd)
    return ligand / (kd + ligand)
end

function target_engagement(signal_control, signal_treated, signal_max)
    return (signal_control - signal_treated) / (signal_control - signal_max)
end

println("response=", round(dose_response(1.0, 1.5, 1.2, 0.05, 1.0), digits=6))
println("occupancy=", round(occupancy(2.0, 2.0), digits=6))
println("target_engagement=", round(target_engagement(100.0, 55.0, 20.0), digits=6))
