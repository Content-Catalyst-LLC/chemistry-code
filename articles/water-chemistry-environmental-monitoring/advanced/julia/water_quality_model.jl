# Water Chemistry and Environmental Monitoring
# Julia water-quality pressure and load model.
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

function load_kg_day(concentration, unit, flow_l_s)
    if flow_l_s <= 0
        return 0.0
    end

    if unit == "mg/L"
        return concentration * flow_l_s * 0.0864
    elseif unit == "ug/L"
        return concentration * flow_l_s * 0.0000864
    else
        return 0.0
    end
end

function oxygen_deficit(do_mg_l, saturation_mg_l)
    return max(saturation_mg_l - do_mg_l, 0.0)
end

function oxygen_stress(do_mg_l, saturation_mg_l)
    low_do = clamp01((6.0 - do_mg_l) / 6.0)
    deficit = clamp01(oxygen_deficit(do_mg_l, saturation_mg_l) / 6.0)
    return clamp01(0.60 * low_do + 0.40 * deficit)
end

function nutrient_index(nitrate_mg_l, phosphate_mg_l)
    return clamp01(0.50 * clamp01(nitrate_mg_l / 10.0) +
                   0.50 * clamp01(phosphate_mg_l / 0.20))
end

function metal_index(lead_ug_l, copper_ug_l, arsenic_ug_l)
    return clamp01(
        0.34 * clamp01(lead_ug_l / 15.0) +
        0.33 * clamp01(copper_ug_l / 13.0) +
        0.33 * clamp01(arsenic_ug_l / 10.0)
    )
end

function turbidity_pressure(turbidity_ntu)
    return clamp01(turbidity_ntu / 100.0)
end

function conductivity_pressure(conductance_us_cm)
    return clamp01((conductance_us_cm - 750.0) / 3000.0)
end

function water_quality_pressure(record)
    site, water_body, analyte, concentration, benchmark, unit, flow,
    do_mg_l, do_sat, nitrate, phosphate, lead, copper, arsenic,
    turbidity, conductance, qc = record

    ratio_component = clamp01(log1p(benchmark_ratio(concentration, benchmark)) / log(4.0))
    oxygen_component = oxygen_stress(do_mg_l, do_sat)
    nutrient_component = nutrient_index(nitrate, phosphate)
    metal_component = metal_index(lead, copper, arsenic)
    turbidity_component = turbidity_pressure(turbidity)
    ionic_component = conductivity_pressure(conductance)
    qc_penalty = 1.0 - qc

    return clamp01(
        0.20 * ratio_component +
        0.18 * oxygen_component +
        0.18 * nutrient_component +
        0.16 * metal_component +
        0.12 * turbidity_component +
        0.08 * ionic_component +
        0.08 * qc_penalty
    )
end

records = [
    ("River-A", "river", "nitrate_as_N", 7.8, 10.0, "mg/L", 820.0, 8.2, 10.2, 7.8, 0.18, 3.0, 5.0, 2.5, 12.0, 540.0, 0.93),
    ("Lake-B", "lake", "dissolved_oxygen", 4.6, 5.0, "mg/L", 0.0, 4.6, 8.5, 1.8, 0.12, 2.0, 4.0, 1.5, 18.0, 420.0, 0.88),
    ("Well-C", "aquifer", "arsenic", 12.0, 10.0, "ug/L", 5.0, 1.1, 9.8, 0.2, 0.02, 1.0, 2.0, 12.0, 0.5, 680.0, 0.86),
    ("Storm-D", "urban_runoff", "lead", 18.0, 15.0, "ug/L", 210.0, 6.4, 9.1, 4.5, 0.42, 18.0, 21.0, 3.0, 75.0, 920.0, 0.80)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_water_quality_model.csv")
open(outfile, "w") do io
    println(io, "site,water_body,analyte,benchmark_ratio,load_kg_day,oxygen_stress,nutrient_index,metal_index,water_quality_pressure")
    for r in records
        site = r[1]
        water_body = r[2]
        analyte = r[3]
        concentration = r[4]
        benchmark = r[5]
        unit = r[6]
        flow = r[7]
        do_mg_l = r[8]
        do_sat = r[9]
        nitrate = r[10]
        phosphate = r[11]
        lead = r[12]
        copper = r[13]
        arsenic = r[14]

        println(io, "$site,$water_body,$analyte,$(benchmark_ratio(concentration, benchmark)),$(load_kg_day(concentration, unit, flow)),$(oxygen_stress(do_mg_l, do_sat)),$(nutrient_index(nitrate, phosphate)),$(metal_index(lead, copper, arsenic)),$(water_quality_pressure(r))")
    end
end

println("Julia water quality model complete: $outfile")
