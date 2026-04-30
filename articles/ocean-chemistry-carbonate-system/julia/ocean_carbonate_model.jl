# Ocean Chemistry and the Carbonate System
# Julia carbonate-system proxy and acidification scenario model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function hydrogen_ion_from_pH(pH)
    return 10.0^(-pH)
end

function alkalinity_dic_ratio(alkalinity, dic)
    if dic <= 0
        return 0.0
    end
    return alkalinity / dic
end

function carbonate_buffer_proxy(pH, alkalinity, dic)
    ratio = alkalinity_dic_ratio(alkalinity, dic)
    pH_component = clamp01((pH - 7.6) / 0.7)
    ratio_component = clamp01((ratio - 1.0) / 0.20)
    return clamp01(0.55 * pH_component + 0.45 * ratio_component)
end

function aragonite_saturation_proxy(carbonate_umol_kg, calcium_mmol_kg, ksp_proxy)
    calcium_umol_kg = calcium_mmol_kg * 1000.0
    if ksp_proxy <= 0
        return 0.0
    end
    return (carbonate_umol_kg * calcium_umol_kg) / (ksp_proxy * 100000.0)
end

function calcite_saturation_proxy(carbonate_umol_kg, calcium_mmol_kg, ksp_proxy)
    calcium_umol_kg = calcium_mmol_kg * 1000.0
    if ksp_proxy <= 0
        return 0.0
    end
    return (carbonate_umol_kg * calcium_umol_kg) / (ksp_proxy * 100000.0)
end

function acidification_pressure(pH, pco2, carbonate_umol_kg, omega_aragonite)
    pH_component = clamp01((8.2 - pH) / 0.7)
    co2_component = clamp01((pco2 - 400.0) / 800.0)
    carbonate_component = clamp01((180.0 - carbonate_umol_kg) / 180.0)
    saturation_component = clamp01((3.0 - omega_aragonite) / 3.0)

    return clamp01(
        0.30 * pH_component +
        0.25 * co2_component +
        0.25 * carbonate_component +
        0.20 * saturation_component
    )
end

function deoxygenation_pressure(oxygen_umol_kg)
    return clamp01((180.0 - oxygen_umol_kg) / 180.0)
end

function nutrient_upwelling_index(nitrate, phosphate, silicate)
    return clamp01(
        0.40 * clamp01(nitrate / 35.0) +
        0.30 * clamp01(phosphate / 3.0) +
        0.30 * clamp01(silicate / 60.0)
    )
end

function carbonate_system_pressure(record)
    id, region, water_mass, temp, salinity, pH, alkalinity, dic, pco2,
    carbonate, calcium, phosphate, nitrate, silicate, oxygen, depth, arag_ksp, calcite_ksp, qc = record

    omega_arag = aragonite_saturation_proxy(carbonate, calcium, arag_ksp)
    acid = acidification_pressure(pH, pco2, carbonate, omega_arag)
    deoxy = deoxygenation_pressure(oxygen)
    nutrients = nutrient_upwelling_index(nitrate, phosphate, silicate)
    buffer = carbonate_buffer_proxy(pH, alkalinity, dic)
    qc_penalty = 1.0 - qc

    return clamp01(
        0.36 * acid +
        0.20 * deoxy +
        0.16 * nutrients +
        0.18 * (1.0 - buffer) +
        0.10 * qc_penalty
    )
end

records = [
    ("OCNFS001", "North_Atlantic", "surface_subpolar", 8.5, 35.1, 8.08, 2310.0, 2060.0, 415.0, 185.0, 10.3, 0.8, 6.2, 3.0, 255.0, 20.0, 60.0, 42.0, 0.94),
    ("OCNFS002", "Equatorial_Pacific", "surface_upwelling", 24.0, 34.8, 7.92, 2285.0, 2130.0, 520.0, 145.0, 10.2, 1.9, 14.5, 8.0, 210.0, 30.0, 60.0, 42.0, 0.91),
    ("OCNFS005", "Arabian_Sea", "oxygen_minimum_zone", 12.0, 35.0, 7.62, 2320.0, 2265.0, 1050.0, 62.0, 10.2, 3.2, 38.0, 28.0, 18.0, 600.0, 60.0, 42.0, 0.84),
    ("OCNFS006", "Caribbean_Reef", "surface_tropical", 28.0, 36.2, 8.12, 2380.0, 2040.0, 390.0, 210.0, 10.5, 0.2, 0.4, 1.0, 230.0, 10.0, 60.0, 42.0, 0.93)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_ocean_carbonate_model.csv")
open(outfile, "w") do io
    println(io, "record_id,region,water_mass,alkalinity_dic_ratio,buffer_proxy,omega_aragonite,omega_calcite,acidification_pressure,deoxygenation_pressure,nutrient_upwelling_index,carbonate_system_pressure")
    for r in records
        id, region, water_mass, temp, salinity, pH, alkalinity, dic, pco2, carbonate, calcium, phosphate, nitrate, silicate, oxygen, depth, arag_ksp, calcite_ksp, qc = r
        omega_arag = aragonite_saturation_proxy(carbonate, calcium, arag_ksp)
        omega_calc = calcite_saturation_proxy(carbonate, calcium, calcite_ksp)
        println(io, "$id,$region,$water_mass,$(alkalinity_dic_ratio(alkalinity,dic)),$(carbonate_buffer_proxy(pH,alkalinity,dic)),$omega_arag,$omega_calc,$(acidification_pressure(pH,pco2,carbonate,omega_arag)),$(deoxygenation_pressure(oxygen)),$(nutrient_upwelling_index(nitrate,phosphate,silicate)),$(carbonate_system_pressure(r))")
    end
end

println("Julia ocean carbonate model complete: $outfile")
