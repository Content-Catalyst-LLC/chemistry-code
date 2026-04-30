# Soil Chemistry, Nutrient Cycles, and Land Systems
# Julia soil nutrient balance and land-system pressure model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function ph_stress(pH)
    if pH < 6.0
        return clamp01((6.0 - pH) / 2.0)
    elseif pH > 7.8
        return clamp01((pH - 7.8) / 2.0)
    else
        return 0.0
    end
end

function cec_buffering_score(cec_cmol_kg)
    return clamp01(cec_cmol_kg / 25.0)
end

function organic_matter_score(organic_matter_percent)
    return clamp01(organic_matter_percent / 6.0)
end

function nutrient_balance_index(nitrate_mg_kg, ammonium_mg_kg, available_p_mg_kg, exchangeable_k_mg_kg)
    nitrogen = clamp01((nitrate_mg_kg + ammonium_mg_kg) / 60.0)
    phosphorus = clamp01(available_p_mg_kg / 40.0)
    potassium = clamp01(exchangeable_k_mg_kg / 250.0)
    return clamp01(0.40 * nitrogen + 0.30 * phosphorus + 0.30 * potassium)
end

function salinity_sodicity_pressure(ec_dS_m, sodium_adsorption_ratio)
    salinity = clamp01((ec_dS_m - 2.0) / 6.0)
    sodicity = clamp01((sodium_adsorption_ratio - 6.0) / 12.0)
    return max(salinity, sodicity)
end

function leaching_pressure(sand_fraction, rainfall_index, nitrate_mg_kg, cec_cmol_kg, organic_matter_percent)
    texture = clamp01(sand_fraction)
    nitrate = clamp01(nitrate_mg_kg / 50.0)
    buffering = 0.5 * cec_buffering_score(cec_cmol_kg) + 0.5 * organic_matter_score(organic_matter_percent)
    return clamp01(0.40 * texture + 0.35 * rainfall_index + 0.25 * nitrate - 0.25 * buffering)
end

function carbon_stability_score(clay_fraction, organic_matter_percent, erosion_risk)
    clay_protection = clamp01(clay_fraction)
    organic = organic_matter_score(organic_matter_percent)
    return clamp01(0.45 * clay_protection + 0.40 * organic + 0.15 * (1.0 - erosion_risk))
end

function soil_system_pressure(row)
    site, land_use, pH, organic_matter, cec, nitrate, ammonium, p, k, ec, sar,
    clay, sand, rainfall, erosion, compaction, qc = row

    nutrient = nutrient_balance_index(nitrate, ammonium, p, k)
    leaching = leaching_pressure(sand, rainfall, nitrate, cec, organic_matter)
    salinity = salinity_sodicity_pressure(ec, sar)
    acidity = ph_stress(pH)
    carbon_stability = carbon_stability_score(clay, organic_matter, erosion)
    qc_penalty = 1.0 - qc

    return clamp01(
        0.18 * (1.0 - nutrient) +
        0.18 * leaching +
        0.16 * salinity +
        0.14 * acidity +
        0.14 * erosion +
        0.10 * compaction +
        0.07 * (1.0 - carbon_stability) +
        0.03 * qc_penalty
    )
end

records = [
    ("Prairie-A", "cropland", 6.4, 4.8, 22.0, 18.0, 6.0, 28.0, 190.0, 0.8, 2.0, 0.34, 0.28, 0.55, 0.22, 0.18, 0.94),
    ("Field-B", "intensive_cropland", 5.5, 2.1, 9.0, 42.0, 8.0, 18.0, 110.0, 1.4, 4.0, 0.18, 0.62, 0.78, 0.46, 0.35, 0.88),
    ("Irrigated-C", "irrigated_agriculture", 8.2, 1.6, 14.0, 25.0, 5.0, 32.0, 210.0, 5.8, 12.0, 0.22, 0.44, 0.40, 0.30, 0.25, 0.86),
    ("Forest-D", "forest", 5.9, 7.2, 18.0, 4.0, 3.0, 9.0, 160.0, 0.3, 1.0, 0.42, 0.30, 0.60, 0.12, 0.10, 0.92),
    ("Degraded-E", "degraded_land", 5.1, 0.9, 5.0, 8.0, 2.0, 5.0, 70.0, 2.2, 8.0, 0.10, 0.72, 0.80, 0.82, 0.65, 0.78)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_soil_nutrient_balance_model.csv")
open(outfile, "w") do io
    println(io, "site,land_use,pH_stress,nutrient_balance_index,leaching_pressure,salinity_sodicity_pressure,carbon_stability_score,soil_system_pressure")
    for r in records
        site = r[1]
        land_use = r[2]
        pH = r[3]
        organic = r[4]
        cec = r[5]
        nitrate = r[6]
        ammonium = r[7]
        p = r[8]
        k = r[9]
        ec = r[10]
        sar = r[11]
        clay = r[12]
        sand = r[13]
        rainfall = r[14]
        erosion = r[15]

        println(io, "$site,$land_use,$(ph_stress(pH)),$(nutrient_balance_index(nitrate,ammonium,p,k)),$(leaching_pressure(sand,rainfall,nitrate,cec,organic)),$(salinity_sodicity_pressure(ec,sar)),$(carbon_stability_score(clay,organic,erosion)),$(soil_system_pressure(r))")
    end
end

println("Julia soil nutrient balance model complete: $outfile")
