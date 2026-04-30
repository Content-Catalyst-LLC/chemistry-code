# Chemistry, Classification, and the Human Understanding of Matter
# Julia chemical classification model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function assign_class(components, phase, charge, contains_metal, coordination_number, is_polymer, network_structure, organic_fraction, ionic_fraction, metallic_fraction, crystalline_score, functional_group)
    if components > 3
        return phase == "heterogeneous_mixture" ? "heterogeneous_mixture" : "mixture_or_solution"
    elseif is_polymer == 1
        return "polymer_material"
    elseif contains_metal == 1 && coordination_number >= 4 && functional_group == "coordination_complex"
        return "coordination_compound"
    elseif ionic_fraction >= 0.65 && crystalline_score >= 0.65
        return "ionic_or_salt_crystal"
    elseif network_structure == 1 && (phase == "crystalline_solid" || phase == "amorphous_solid")
        return "extended_solid_or_network_material"
    elseif organic_fraction >= 0.65
        return "organic_molecular_substance"
    elseif metallic_fraction >= 0.40
        return "metallic_or_intermetallic_material"
    else
        return "molecular_or_material_record"
    end
end

function evidence_score(spectral, elemental, thermal, qc)
    return clamp01(0.35 * spectral + 0.30 * elemental + 0.20 * thermal + 0.15 * qc)
end

function classification_reliability(spectral, elemental, thermal, confidence, qc)
    e = evidence_score(spectral, elemental, thermal, qc)
    return clamp01(0.55 * e + 0.30 * confidence + 0.15 * qc)
end

records = [
    ("ethyl_acetate_reference", 1.0, "liquid", 0.0, 0, 0.0, 0, 0, 1.00, 0.00, 0.00, 0.05, "ester", 0.92, 0.88, 0.74, 0.86, 0.94),
    ("seawater_sample", 18.0, "aqueous_solution", 0.0, 1, 0.0, 0, 0, 0.05, 0.78, 0.02, 0.00, "mixed_inorganic_ions", 0.70, 0.82, 0.40, 0.74, 0.90),
    ("sodium_chloride_crystal", 2.0, "crystalline_solid", 0.0, 1, 6.0, 0, 1, 0.00, 0.95, 0.00, 0.96, "halide_salt", 0.88, 0.93, 0.70, 0.91, 0.96),
    ("polyethylene_film", 1.0, "solid", 0.0, 0, 0.0, 1, 0, 1.00, 0.00, 0.00, 0.35, "alkane_polymer", 0.80, 0.68, 0.86, 0.82, 0.92)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_chemical_classification_scores.csv")
open(outfile, "w") do io
    println(io, "sample_name,assigned_class,evidence_score,classification_reliability")
    for r in records
        sample, components, phase, charge, metal, coord, polymer, network, organic, ionic, metallic, crystalline, fg, spectral, elemental, thermal, confidence, qc = r
        cls = assign_class(components, phase, charge, metal, coord, polymer, network, organic, ionic, metallic, crystalline, fg)
        e = evidence_score(spectral, elemental, thermal, qc)
        reliability = classification_reliability(spectral, elemental, thermal, confidence, qc)
        println(io, "$sample,$cls,$e,$reliability")
    end
end

println("Julia chemical classification model complete: $outfile")
