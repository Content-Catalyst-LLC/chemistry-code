# Environmental Chemistry and the Chemical Conditions of Habitability
# Julia multimedia partitioning and habitability pressure model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function benchmark_ratio(concentration, benchmark)
    if benchmark <= 0
        return 0.0
    end
    return concentration / benchmark
end

function kd_l_kg(koc_l_kg, organic_carbon_fraction)
    return koc_l_kg * organic_carbon_fraction
end

function retardation_factor(kd, bulk_density_g_cm3, porosity)
    n = max(porosity, 0.01)
    return 1.0 + (bulk_density_g_cm3 * kd) / n
end

function mobility_factor(retardation)
    return 1.0 / sqrt(max(retardation, 1.0))
end

function henry_tendency(henry_atm_m3_mol)
    return clamp01(log1p(max(henry_atm_m3_mol, 0.0) * 1000.0) / log(20.0))
end

function persistence_factor(half_life_days)
    return half_life_days / (half_life_days + 90.0)
end

function nutrient_pressure(nitrate_mg_l, phosphate_mg_l)
    return clamp01(0.5 * clamp01(nitrate_mg_l / 10.0) +
                   0.5 * clamp01(phosphate_mg_l / 0.20))
end

function habitability_pressure(row)
    name, compartment, analyte_class, concentration, benchmark, koc, foc,
    henry, half_life, bulk_density, porosity, nitrate, phosphate,
    exposure_weight, receptor_sensitivity, qc = row

    ratio_component = clamp01(log1p(benchmark_ratio(concentration, benchmark)) / log(5.0))
    kd = kd_l_kg(koc, foc)
    retardation = retardation_factor(kd, bulk_density, porosity)
    mobility = mobility_factor(retardation)
    volatility = henry_tendency(henry)
    persistence = persistence_factor(half_life)
    nutrient = nutrient_pressure(nitrate, phosphate)
    qc_penalty = 1.0 - qc

    return clamp01(
        0.22 * ratio_component +
        0.15 * mobility +
        0.12 * volatility +
        0.15 * persistence +
        0.14 * nutrient +
        0.12 * exposure_weight +
        0.07 * receptor_sensitivity +
        0.03 * qc_penalty
    )
end

records = [
    ("arsenic_groundwater", "groundwater", "metalloid", 13.5, 10.0, 120.0, 0.002, 1e-12, 99999.0, 1.65, 0.32, 0.3, 0.02, 0.95, 0.90, 0.88),
    ("pyrene_sediment", "sediment", "pah", 1.9, 1.0, 60000.0, 0.055, 1.2e-6, 220.0, 1.15, 0.58, 1.1, 0.08, 0.55, 0.82, 0.80),
    ("TCE_groundwater", "groundwater", "chlorinated_solvent", 8.5, 5.0, 90.0, 0.001, 0.0091, 365.0, 1.70, 0.30, 0.1, 0.01, 0.93, 0.91, 0.83),
    ("phosphate_wetland", "wetland_water", "nutrient", 0.21, 0.10, 80.0, 0.012, 1e-12, 45.0, 1.0, 0.95, 1.6, 0.21, 0.62, 0.80, 0.89)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_environmental_partition_model.csv")
open(outfile, "w") do io
    println(io, "record,compartment,Kd_L_kg,retardation_factor,mobility_factor,henry_tendency,persistence_factor,habitability_pressure")
    for row in records
        name = row[1]
        compartment = row[2]
        koc = row[6]
        foc = row[7]
        henry = row[8]
        half_life = row[9]
        bulk_density = row[10]
        porosity = row[11]
        kd = kd_l_kg(koc, foc)
        retardation = retardation_factor(kd, bulk_density, porosity)
        println(io, "$name,$compartment,$kd,$retardation,$(mobility_factor(retardation)),$(henry_tendency(henry)),$(persistence_factor(half_life)),$(habitability_pressure(row))")
    end
end

println("Julia environmental partition model complete: $outfile")
