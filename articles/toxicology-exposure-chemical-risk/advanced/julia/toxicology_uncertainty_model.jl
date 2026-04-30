# Toxicology, Exposure, and Chemical Risk
# Julia probabilistic exposure and hazard-index example.
# Synthetic educational code only.

using Random
using Statistics

function chronic_daily_intake(concentration, intake_rate, exposure_frequency, exposure_duration, body_weight, averaging_time)
    return concentration * intake_rate * exposure_frequency * exposure_duration / (body_weight * averaging_time)
end

function absorbed_dose(cdi, absorption_fraction)
    return cdi * absorption_fraction
end

function hazard_quotient(dose, reference_dose)
    if reference_dose <= 0.0
        return 0.0
    end
    return dose / reference_dose
end

function cancer_risk_proxy(dose, slope_factor)
    return dose * slope_factor
end

function monte_carlo_hq(; concentration, intake_rate, exposure_frequency, exposure_duration, body_weight, averaging_time, absorption_fraction, reference_dose, draws=1000, seed=42)
    Random.seed!(seed)
    values = Float64[]

    for _ in 1:draws
        c = concentration * exp(randn() * 0.25)
        ir = intake_rate * exp(randn() * 0.20)
        bw = body_weight * exp(randn() * 0.10)
        rfd = reference_dose * exp(randn() * 0.35)

        cdi = chronic_daily_intake(c, ir, exposure_frequency, exposure_duration, bw, averaging_time)
        dose = absorbed_dose(cdi, absorption_fraction)
        push!(values, hazard_quotient(dose, rfd))
    end

    sorted = sort(values)
    return (
        p05 = sorted[Int(round(0.05 * (draws - 1))) + 1],
        p50 = median(sorted),
        p95 = sorted[Int(round(0.95 * (draws - 1))) + 1],
        probability_above_1 = count(x -> x >= 1.0, sorted) / draws
    )
end

records = [
    ("arsenic_water", 0.010, 2.0, 350.0, 30.0, 70.0, 10950.0, 0.95, 0.0003, 1.5),
    ("lead_soil_dust", 120.0, 0.0001, 180.0, 6.0, 15.0, 2190.0, 0.40, 0.0035, 0.0),
    ("pfos_water", 0.000020, 2.0, 350.0, 30.0, 70.0, 10950.0, 0.90, 0.00000002, 0.0)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_toxicology_uncertainty.csv")

open(outfile, "w") do io
    println(io, "record,cdi,absorbed_dose,hazard_quotient,cancer_risk_proxy,mc_hq_p05,mc_hq_p50,mc_hq_p95,mc_probability_hq_above_1")

    for r in records
        name, c, ir, ef, ed, bw, at, af, rfd, sf = r
        cdi = chronic_daily_intake(c, ir, ef, ed, bw, at)
        dose = absorbed_dose(cdi, af)
        hq = hazard_quotient(dose, rfd)
        risk = cancer_risk_proxy(dose, sf)
        mc = monte_carlo_hq(
            concentration=c,
            intake_rate=ir,
            exposure_frequency=ef,
            exposure_duration=ed,
            body_weight=bw,
            averaging_time=at,
            absorption_fraction=af,
            reference_dose=rfd,
            seed=length(name) * 101
        )

        println(io, "$name,$cdi,$dose,$hq,$risk,$(mc.p05),$(mc.p50),$(mc.p95),$(mc.probability_above_1)")
    end
end

println("Julia toxicology uncertainty model complete: $outfile")
