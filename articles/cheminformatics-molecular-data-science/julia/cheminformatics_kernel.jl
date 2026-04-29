# Cheminformatics numerical kernel in Julia.

function tanimoto(a, b, c)
    return c / (a + b - c)
end

function pic50(ic50_nm)
    ic50_m = ic50_nm * 1.0e-9
    return -log10(ic50_m)
end

function euclidean_distance(x, y)
    return sqrt(sum((x .- y).^2))
end

println("tanimoto=", round(tanimoto(5.0, 4.0, 3.0), digits=6))
println("pIC50=", round(pic50(50.0), digits=6))
println("distance=", round(euclidean_distance([1.0, 2.0, 3.0], [1.5, 2.5, 4.0]), digits=6))
