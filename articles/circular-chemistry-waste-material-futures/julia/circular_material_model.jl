# Circular Chemistry, Waste, and Material Futures
# Julia circular material flow and retention model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function recovery_yield(recovered, input)
    input <= 0 ? 0.0 : recovered / input
end

function circular_retention(recovery, quality, substitution)
    recovery * quality * substitution
end

function material_remaining(initial_mass, loss_fraction, cycles)
    initial_mass * (1.0 - loss_fraction)^cycles
end

function hazard_weighted_flow(recovered, hazard, exposure)
    recovered * hazard * exposure
end

function energy_intensity(energy, recovered)
    recovered <= 0 ? 0.0 : energy / recovered
end

function safe_circularity(hazard, exposure, contamination, worker_exposure)
    clamp01(0.30 * (1.0 - hazard) + 0.25 * (1.0 - exposure) + 0.25 * (1.0 - contamination) + 0.20 * (1.0 - worker_exposure))
end

function circular_score(row)
    name, input, recovered, quality, substitution, energy, reagent, water, hazard, exposure, contamination, traceability, collection, sorting, cycles, loss, critical, worker = row

    rec = recovery_yield(recovered, input)
    retention = circular_retention(rec, quality, substitution)
    infrastructure = clamp01(0.45 * collection + 0.40 * sorting + 0.15 * traceability)
    safety = safe_circularity(hazard, exposure, contamination, worker)
    energy_score = clamp01(1.0 - energy_intensity(energy, recovered) / 2.0)
    reagent_score = clamp01(1.0 - (recovered <= 0 ? 0.0 : reagent / recovered) / 0.6)
    critical_value = clamp01(critical * substitution)

    return clamp01(0.18 * rec + 0.20 * retention + 0.14 * infrastructure + 0.16 * safety + 0.10 * energy_score + 0.08 * reagent_score + 0.08 * critical_value + 0.06 * traceability)
end

streams = [
    ("PET_bottles_clear", 1000.0, 760.0, 0.82, 0.72, 180.0, 12.0, 90.0, 0.18, 0.22, 0.18, 0.78, 0.68, 0.74, 3.0, 0.12, 0.00, 0.20),
    ("Lithium_ion_batteries", 500.0, 310.0, 0.78, 0.72, 520.0, 160.0, 220.0, 0.48, 0.55, 0.40, 0.70, 0.52, 0.64, 2.0, 0.18, 0.42, 0.58),
    ("Solvent_wash_stream", 1500.0, 1260.0, 0.88, 0.86, 340.0, 20.0, 30.0, 0.32, 0.46, 0.20, 0.75, 0.80, 0.90, 10.0, 0.08, 0.00, 0.42)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_circular_material_scores.csv")
open(outfile, "w") do io
    println(io, "stream,recovery_yield,circular_retention,material_remaining_after_cycles,hazard_weighted_flow,energy_intensity,circular_score")
    for s in streams
        name = s[1]
        rec = recovery_yield(s[3], s[2])
        retention = circular_retention(rec, s[4], s[5])
        remaining = material_remaining(s[2], s[16], s[15])
        hazard_flow = hazard_weighted_flow(s[3], s[9], s[10])
        energy = energy_intensity(s[6], s[3])
        score = circular_score(s)
        println(io, "$name,$rec,$retention,$remaining,$hazard_flow,$energy,$score")
    end
end

println("Julia circular material model complete: $outfile")
