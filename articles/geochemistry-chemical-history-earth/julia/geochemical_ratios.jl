# Geochemistry educational calculations in Julia.
# Includes simplified CIA, isotope delta notation, radiometric age,
# and two-component mixing.

using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

function cia_simplified(al2o3, cao, na2o, k2o)
    return 100.0 * al2o3 / (al2o3 + cao + na2o + k2o)
end

function isotope_delta(sample_ratio, standard_ratio)
    return ((sample_ratio / standard_ratio) - 1.0) * 1000.0
end

function radiometric_age_ma(parent, daughter, lambda)
    return (1.0 / lambda) * log(1.0 + daughter / parent) / 1.0e6
end

function two_component_mix(f, c1, c2)
    return f * c1 + (1.0 - f) * c2
end

cases = [
    ("basalt", 15.4, 10.5, 2.9, 0.8),
    ("granite", 14.1, 1.8, 3.6, 4.8),
    ("weathered_saprolite", 25.5, 0.8, 0.3, 1.2)
]

open(joinpath(table_dir, "julia_cia_examples.csv"), "w") do io
    println(io, "rock_type,Al2O3,CaO,Na2O,K2O,CIA_simplified")
    for (rock_type, al, ca, na, k) in cases
        println(io, "$(rock_type),$(al),$(ca),$(na),$(k),$(cia_simplified(al, ca, na, k))")
    end
end

delta_c = isotope_delta(0.01112, 0.01118)
age_ma = radiometric_age_ma(1.0, 0.35, 1.55125e-10)
mixed_sr = two_component_mix(0.35, 420.0, 160.0)

@printf("Delta carbon example: %.3f per mil\n", delta_c)
@printf("Simplified radiometric age: %.2f Ma\n", age_ma)
@printf("Two-component Sr mix: %.2f ppm\n", mixed_sr)
println("Julia geochemistry workflow complete.")
