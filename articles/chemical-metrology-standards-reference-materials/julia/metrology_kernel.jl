# Chemical metrology numerical kernel in Julia.

function combined_standard_uncertainty(components)
    return sqrt(sum(x -> x^2, components))
end

function expanded_uncertainty(uc, k)
    return k * uc
end

function normalized_error(x_lab, x_ref, u_lab, u_ref)
    return (x_lab - x_ref) / sqrt(u_lab^2 + u_ref^2)
end

components = [0.004, 0.006, 0.010, 0.015, 0.012, 0.020]
uc = combined_standard_uncertainty(components)
U = expanded_uncertainty(uc, 2.0)
en = normalized_error(10.2, 10.0, 0.8, 0.4)

println("combined_standard_uncertainty=", round(uc, digits=6))
println("expanded_uncertainty=", round(U, digits=6))
println("normalized_error=", round(en, digits=6))
