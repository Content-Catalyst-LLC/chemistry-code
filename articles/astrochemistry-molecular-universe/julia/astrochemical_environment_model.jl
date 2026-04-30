# Astrochemistry and the Molecular Universe
# Julia molecular-cloud, ice, and astrochemical environment model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function arrhenius_like_rate(alpha, activation_k, temperature_k)
    if temperature_k <= 0
        return 0.0
    end
    return alpha * exp(-activation_k / temperature_k)
end

function uv_attenuation(uv_field_g0, visual_extinction_mag)
    return uv_field_g0 * exp(-1.8 * visual_extinction_mag)
end

function attenuated_photodissociation_rate(base_rate_s, uv_field_g0, visual_extinction_mag)
    return base_rate_s * uv_attenuation(uv_field_g0, visual_extinction_mag)
end

function freezeout_efficiency(density_cm3, dust_temperature_k, binding_energy_k)
    density_component = clamp01(log10(max(density_cm3, 1.0)) / 8.0)
    thermal_retention = clamp01(binding_energy_k / max(100.0 * dust_temperature_k, 1.0))
    return clamp01(0.55 * density_component + 0.45 * thermal_retention)
end

function thermal_desorption_proxy(binding_energy_k, dust_temperature_k)
    if dust_temperature_k <= 0
        return 0.0
    end
    return clamp01(exp(-binding_energy_k / dust_temperature_k) * 1.0e8)
end

function ionization_pressure(cosmic_ray_ionization_s)
    return clamp01(log10(max(cosmic_ray_ionization_s, 1e-20) / 1e-18) / 4.0)
end

function molecular_complexity_score(organic_complexity, column_density_cm2, metallicity_proxy)
    column_component = clamp01(log10(max(column_density_cm2, 1.0)) / 18.0)
    return clamp01(0.45 * organic_complexity + 0.35 * column_component + 0.20 * metallicity_proxy)
end

function ice_chemistry_score(ice_fraction, water_ice_index, freezeout)
    return clamp01(0.40 * ice_fraction + 0.35 * water_ice_index + 0.25 * freezeout)
end

function astrochemical_activity(record)
    id, region, environment, family, species, gas_temp, dust_temp, density, column_density,
    uv, cosmic_ray, av, binding, photorate, formation, desorb_yield, ice_fraction,
    water_ice, organic_complexity, deuteration, metallicity, qc = record

    attenuation = uv_attenuation(uv, av)
    photo = attenuated_photodissociation_rate(photorate, uv, av)
    freezeout = freezeout_efficiency(density, dust_temp, binding)
    desorption = thermal_desorption_proxy(binding, dust_temp)
    ionization = ionization_pressure(cosmic_ray)
    complexity = molecular_complexity_score(organic_complexity, column_density, metallicity)
    ice = ice_chemistry_score(ice_fraction, water_ice, freezeout)
    qc_penalty = 1.0 - qc

    return clamp01(
        0.18 * complexity +
        0.17 * ice +
        0.16 * ionization +
        0.14 * clamp01(log10(max(formation, 1e-20) / 1e-12) / 4.0) +
        0.13 * clamp01(desorb_yield) +
        0.10 * deuteration +
        0.07 * clamp01(attenuation / 10.0) +
        0.05 * qc_penalty -
        0.08 * clamp01(photo / 1e-8)
    )
end

records = [
    ("ASTFS001", "Taurus_TMC1", "cold_dark_cloud", "carbon_chain", "HC3N", 10.0, 8.0, 120000.0, 2.2e13, 0.05, 1.3e-17, 12.0, 3600.0, 1.0e-11, 2.0e-10, 0.02, 0.72, 0.65, 0.54, 0.08, 1.00, 0.93),
    ("ASTFS002", "Orion_KL", "hot_core", "complex_organic", "CH3OCH3", 150.0, 120.0, 5000000.0, 8.0e15, 10.0, 5.0e-16, 8.0, 4200.0, 3.0e-10, 8.0e-10, 0.18, 0.35, 0.42, 0.92, 0.03, 1.15, 0.90),
    ("ASTFS003", "Protoplanetary_Disk_TW_Hya", "disk_midplane", "ice_chemistry", "H2O_ice", 25.0, 18.0, 100000000.0, 1.0e18, 0.20, 1.0e-17, 20.0, 5700.0, 1.0e-12, 1.5e-10, 0.03, 0.88, 0.95, 0.30, 0.12, 1.00, 0.91),
    ("ASTFS007", "Sgr_B2_N", "hot_core", "complex_organic", "CH3OH", 120.0, 100.0, 3000000.0, 2.5e17, 20.0, 6.0e-16, 10.0, 5500.0, 2.0e-10, 9.0e-10, 0.25, 0.42, 0.58, 0.86, 0.05, 1.20, 0.89)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_astrochemical_environment_model.csv")
open(outfile, "w") do io
    println(io, "record_id,region,environment,species,uv_attenuation,attenuated_photodissociation_rate,freezeout_efficiency,thermal_desorption_proxy,ionization_pressure,molecular_complexity_score,ice_chemistry_score,astrochemical_activity")
    for r in records
        id, region, environment, family, species, gas_temp, dust_temp, density, column_density,
        uv, cosmic_ray, av, binding, photorate, formation, desorb_yield, ice_fraction,
        water_ice, organic_complexity, deuteration, metallicity, qc = r

        freezeout = freezeout_efficiency(density, dust_temp, binding)
        println(io, "$id,$region,$environment,$species,$(uv_attenuation(uv,av)),$(attenuated_photodissociation_rate(photorate,uv,av)),$freezeout,$(thermal_desorption_proxy(binding,dust_temp)),$(ionization_pressure(cosmic_ray)),$(molecular_complexity_score(organic_complexity,column_density,metallicity)),$(ice_chemistry_score(ice_fraction,water_ice,freezeout)),$(astrochemical_activity(r))")
    end
end

println("Julia astrochemical environment model complete: $outfile")
