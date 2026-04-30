# Food Chemistry and the Molecular Basis of Nutrition
# Julia food-matrix modeling example.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function nutrient_density(protein_g, fiber_g, potassium_mg, calcium_mg, iron_mg, energy_kcal)
    beneficial =
        0.28 * clamp01(protein_g / 25.0) +
        0.24 * clamp01(fiber_g / 12.0) +
        0.18 * clamp01(potassium_mg / 800.0) +
        0.16 * clamp01(calcium_mg / 400.0) +
        0.14 * clamp01(iron_mg / 6.0)

    energy_factor = max(energy_kcal / 100.0, 0.5)
    return beneficial / energy_factor
end

function glycemic_accessibility(starch_g, sugars_g, fiber_g, particle_accessibility, processing_intensity)
    starch_component = clamp01(starch_g / 30.0)
    sugar_component = clamp01(sugars_g / 20.0)
    fiber_protection = clamp01(fiber_g / 12.0)

    return clamp01(
        0.32 * starch_component +
        0.24 * sugar_component +
        0.22 * particle_accessibility +
        0.16 * processing_intensity -
        0.20 * fiber_protection
    )
end

function bioavailable_iron(iron_mg, retention_factor, bioavailability_factor)
    return iron_mg * retention_factor * bioavailability_factor
end

foods = [
    ("lentils_cooked", 230.0, 18.0, 15.0, 730.0, 38.0, 6.6, 22.0, 3.0, 0.45, 0.25, 0.88, 0.16),
    ("oats_cooked", 180.0, 10.0, 8.0, 180.0, 25.0, 3.0, 18.0, 1.0, 0.50, 0.30, 0.90, 0.10),
    ("spinach_cooked", 45.0, 5.0, 4.0, 840.0, 245.0, 6.4, 0.0, 1.0, 0.62, 0.35, 0.72, 0.07),
    ("walnuts", 330.0, 15.0, 7.0, 320.0, 65.0, 1.4, 2.0, 2.0, 0.35, 0.20, 0.86, 0.08)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_food_matrix_scores.csv")
open(outfile, "w") do io
    println(io, "food,energy_kcal,nutrient_density,glycemic_accessibility,bioavailable_iron_mg")
    for f in foods
        food, energy, protein, fiber, potassium, calcium, iron, starch, sugars, particle, processing, retention, bioavailability = f
        nd = nutrient_density(protein, fiber, potassium, calcium, iron, energy)
        ga = glycemic_accessibility(starch, sugars, fiber, particle, processing)
        bi = bioavailable_iron(iron, retention, bioavailability)
        println(io, "$food,$energy,$nd,$ga,$bi")
    end
end

println("Julia food matrix model complete: $outfile")
