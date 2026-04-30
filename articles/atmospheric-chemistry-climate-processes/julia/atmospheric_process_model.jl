# Atmospheric Chemistry and Climate Processes
# Julia greenhouse forcing, ozone, and aerosol sensitivity model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function reference_ratio(concentration, reference)
    if reference <= 0
        return 0.0
    end
    return concentration / reference
end

function greenhouse_forcing_proxy(species, concentration, reference)
    if concentration <= 0 || reference <= 0
        return 0.0
    end

    if species == "CO2"
        return 5.35 * log(concentration / reference)
    elseif species == "CH4"
        return 0.036 * (sqrt(concentration) - sqrt(reference))
    elseif species == "N2O"
        return 0.12 * (sqrt(concentration) - sqrt(reference))
    else
        return 0.0
    end
end

function photochemical_ozone_index(nox_ppb, voc_ppb, sunlight_index)
    if nox_ppb <= 0 || voc_ppb <= 0
        return 0.0
    end
    return sqrt(nox_ppb * voc_ppb) * sunlight_index
end

function aerosol_direct_effect_proxy(aod, single_scattering_albedo)
    scattering = -25.0 * aod * single_scattering_albedo
    absorption = 12.0 * aod * (1.0 - single_scattering_albedo)
    return scattering + absorption
end

function persistence_factor(lifetime_days)
    return lifetime_days / (lifetime_days + 30.0)
end

function atmospheric_pressure(record)
    id, species, class_name, concentration, reference, nox, voc, sunlight, aod, ssa, lifetime, qc = record

    ratio_component = clamp01(log1p(reference_ratio(concentration, reference)) / log(4.0))
    forcing_component = clamp01(abs(greenhouse_forcing_proxy(species, concentration, reference)) / 4.0)
    ozone_component = clamp01(photochemical_ozone_index(nox, voc, sunlight) / 100.0)
    aerosol_component = clamp01(abs(aerosol_direct_effect_proxy(aod, ssa)) / 20.0)
    persistence_component = persistence_factor(lifetime)
    qc_penalty = 1.0 - qc

    if class_name == "greenhouse_gas"
        return clamp01(0.28 * ratio_component + 0.34 * forcing_component + 0.25 * persistence_component + 0.08 * ozone_component + 0.05 * qc_penalty)
    elseif class_name == "aerosol"
        return clamp01(0.24 * ratio_component + 0.34 * aerosol_component + 0.18 * persistence_component + 0.14 * ozone_component + 0.10 * qc_penalty)
    else
        return clamp01(0.26 * ratio_component + 0.36 * ozone_component + 0.14 * aerosol_component + 0.14 * persistence_component + 0.10 * qc_penalty)
    end
end

records = [
    ("ATMFS001", "CO2", "greenhouse_gas", 423.0, 280.0, 0.0, 0.0, 1.0, 0.04, 0.96, 36500.0, 0.95),
    ("ATMFS002", "CH4", "greenhouse_gas", 1950.0, 722.0, 0.0, 0.0, 1.0, 0.03, 0.95, 4380.0, 0.94),
    ("ATMFS004", "O3", "secondary_pollutant", 0.078, 0.070, 38.0, 85.0, 1.15, 0.08, 0.93, 0.20, 0.90),
    ("ATMFS006", "PM2.5", "aerosol", 38.0, 15.0, 22.0, 95.0, 0.75, 0.68, 0.86, 5.0, 0.84)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_atmospheric_process_model.csv")
open(outfile, "w") do io
    println(io, "record_id,species,chemical_class,reference_ratio,forcing_proxy,ozone_index,aerosol_effect,persistence_factor,atmospheric_pressure")
    for r in records
        id, species, class_name, concentration, reference, nox, voc, sunlight, aod, ssa, lifetime, qc = r
        println(io, "$id,$species,$class_name,$(reference_ratio(concentration, reference)),$(greenhouse_forcing_proxy(species, concentration, reference)),$(photochemical_ozone_index(nox, voc, sunlight)),$(aerosol_direct_effect_proxy(aod, ssa)),$(persistence_factor(lifetime)),$(atmospheric_pressure(r))")
    end
end

println("Julia atmospheric process model complete: $outfile")
