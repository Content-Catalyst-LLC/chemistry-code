# Acid-base numerical kernel in Julia.

const KW = 1.0e-14

function weak_acid_hydronium(Ka, C)
    return (-Ka + sqrt(Ka^2 + 4.0 * Ka * C)) / 2.0
end

function ph_from_hydronium(H)
    return -log10(H)
end

function henderson_hasselbalch(pKa, base, acid)
    return pKa + log10(base / acid)
end

H = weak_acid_hydronium(1.8e-5, 0.100)
pH = ph_from_hydronium(H)
buffer_pH = henderson_hasselbalch(4.76, 0.120, 0.100)

println("weak_acid_hydronium=", round(H, digits=8))
println("weak_acid_pH=", round(pH, digits=6))
println("buffer_pH=", round(buffer_pH, digits=6))
