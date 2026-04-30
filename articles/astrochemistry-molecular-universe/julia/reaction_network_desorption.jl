# Astrochemistry educational calculations in Julia.
# Includes a simple first-order photodissociation model and thermal desorption.

using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

function photodissociation_remaining(n0, k_ph, t_seconds)
    return n0 * exp(-k_ph * t_seconds)
end

function desorption_rate(binding_energy_K, dust_temperature_K; attempt_frequency=1.0e12)
    return attempt_frequency * exp(-binding_energy_K / dust_temperature_K)
end

function fractional_abundance(column_density, h2_column_density)
    return column_density / h2_column_density
end

species_cases = [
    ("CO", 855.0, 10.0, 2.0e17, 2.0e22),
    ("CH3OH", 5500.0, 120.0, 8.0e16, 5.0e23),
    ("H2O", 5700.0, 160.0, 1.0e17, 5.0e19)
]

open(joinpath(table_dir, "julia_desorption_abundance.csv"), "w") do io
    println(io, "species,binding_energy_K,dust_temperature_K,desorption_rate_s1,fractional_abundance")
    for (species, eb, temp, col, h2col) in species_cases
        println(io, "$(species),$(eb),$(temp),$(desorption_rate(eb, temp)),$(fractional_abundance(col, h2col))")
    end
end

n0 = 1.0e6
k_ph = 1.0e-9
t_seconds = 1.0e7
remaining = photodissociation_remaining(n0, k_ph, t_seconds)

@printf("Remaining molecules after photodissociation example: %.3e\n", remaining)
println("Julia astrochemistry workflow complete.")
