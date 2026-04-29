# Environmental partitioning and river-pulse simulation.
# Educational Julia example for environmental chemistry.

using DelimitedFiles
using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

# Henry-law style air-water partitioning.
# C_air = H * C_water for a simplified dimensionless Henry coefficient.
function air_water_partition(c_water, henry_dimensionless)
    return henry_dimensionless * c_water
end

# First-order pulse concentration.
function first_order_concentration(c0, k, t)
    return c0 * exp(-k * t)
end

# Weak-acid neutral fraction:
# alpha_HA = 1 / (1 + 10^(pH - pKa))
function weak_acid_neutral_fraction(pH, pKa)
    return 1.0 / (1.0 + 10.0^(pH - pKa))
end

# Generate a small river-pulse table.
c0 = 100.0
k = 0.08
days = collect(0:5:90)
rows = [["day" "concentration_ug_L" "fraction_remaining"]]

for day in days
    c = first_order_concentration(c0, k, day)
    rows = vcat(rows, [day c c / c0])
end

outfile = joinpath(table_dir, "julia_river_pulse_decay.csv")
open(outfile, "w") do io
    for row in eachrow(rows)
        println(io, join(row, ","))
    end
end

println("Air-water partitioning example")
@printf("C_air = %.4f when C_water = %.2f and H = %.5f\n", air_water_partition(25.0, 0.003), 25.0, 0.003)

println("Weak-acid neutral fraction example")
for pH in [5.0, 7.0, 9.0]
    @printf("pH %.1f, pKa 6.5, neutral fraction %.4f\n", pH, weak_acid_neutral_fraction(pH, 6.5))
end

println("Wrote: ", outfile)
