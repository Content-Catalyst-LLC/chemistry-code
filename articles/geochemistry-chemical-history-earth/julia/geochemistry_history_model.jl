# Geochemistry and the Chemical History of Earth
# Julia isotope dating, weathering, redox, and geochemical screening model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function decay_constant_from_half_life_ma(half_life_ma)
    if half_life_ma <= 0
        return 0.0
    end
    return log(2.0) / half_life_ma
end

function model_age_from_parent_fraction(parent_fraction, half_life_ma)
    if parent_fraction <= 0 || parent_fraction > 1 || half_life_ma <= 0
        return 0.0
    end
    lambda = decay_constant_from_half_life_ma(half_life_ma)
    return -log(parent_fraction) / lambda
end

function isotope_half_life_ma(parent_isotope)
    if parent_isotope == "Rb87"
        return 48800.0
    elseif parent_isotope == "Sm147"
        return 106000.0
    elseif parent_isotope == "K40"
        return 1250.0
    elseif parent_isotope == "U238"
        return 4468.0
    else
        return 0.0
    end
end

function chemical_index_of_alteration(al2o3, cao, na2o, k2o)
    denominator = al2o3 + cao + na2o + k2o
    if denominator <= 0
        return 0.0
    end
    return 100.0 * al2o3 / denominator
end

function mafic_index(mgo, feo, tio2, sio2)
    mafic = mgo + feo + tio2
    total = mafic + sio2
    if total <= 0
        return 0.0
    end
    return mafic / total
end

function crustal_evolution_proxy(sio2, rb, sr, epsilon_nd, initial_sr)
    silica = clamp01((sio2 - 45.0) / 30.0)
    rb_sr = rb / max(sr, 0.001)
    evolved_sr = clamp01((initial_sr - 0.703) / 0.020)
    depleted_mantle = clamp01((epsilon_nd + 5.0) / 15.0)
    return clamp01(0.35 * silica + 0.25 * clamp01(rb_sr / 1.5) + 0.25 * evolved_sr + 0.15 * (1.0 - depleted_mantle))
end

function redox_state_proxy(redox_proxy, feo, mno)
    return clamp01(0.65 * redox_proxy + 0.25 * clamp01(feo / 15.0) + 0.10 * clamp01(mno / 0.30))
end

function geochemical_history_pressure(record)
    sample_id, province, rock_type, tectonic, reported_age, parent, daughter,
    parent_fraction, measured_ratio, sio2, al2o3, cao, na2o, k2o, mgo, feo,
    mno, tio2, rb, sr, sm, nd, u, th, pb, d13c, d18o, eps_nd, initial_sr,
    redox, weathering_context, qc = record

    half_life = isotope_half_life_ma(parent)
    model_age = model_age_from_parent_fraction(parent_fraction, half_life)
    age_disagreement = clamp01(abs(model_age - reported_age) / max(reported_age, 1.0))
    cia = chemical_index_of_alteration(al2o3, cao, na2o, k2o)
    weathering = clamp01((cia - 50.0) / 50.0)
    mafic = mafic_index(mgo, feo, tio2, sio2)
    crustal = crustal_evolution_proxy(sio2, rb, sr, eps_nd, initial_sr)
    redox_state = redox_state_proxy(redox, feo, mno)
    qc_penalty = 1.0 - qc

    return clamp01(
        0.18 * age_disagreement +
        0.18 * weathering +
        0.16 * mafic +
        0.18 * crustal +
        0.16 * redox_state +
        0.10 * weathering_context +
        0.04 * qc_penalty
    )
end

records = [
    ("GEOFS001", "Superior_Craton", "granite", "continental_crust", 2700.0, "Rb87", "Sr87", 0.72, 0.39, 72.5, 14.1, 1.8, 3.4, 4.8, 0.6, 1.9, 0.04, 0.31, 185.0, 210.0, 4.2, 22.0, 2.8, 11.5, 18.0, -5.5, 8.7, -6.2, 0.7125, 0.32, 0.25, 0.93),
    ("GEOFS002", "Mid_Ocean_Ridge", "basalt", "oceanic_crust", 5.0, "Sm147", "Nd143", 0.999, 0.5129, 50.2, 15.4, 11.8, 2.8, 0.3, 7.6, 8.9, 0.16, 1.7, 4.0, 120.0, 3.5, 12.0, 0.2, 0.6, 0.5, -4.8, 5.8, 8.1, 0.7028, 0.55, 0.05, 0.95),
    ("GEOFS005", "Himalayan_Foreland", "shale", "sedimentary_basin", 25.0, "Rb87", "Sr87", 0.996, 0.7160, 61.0, 18.5, 1.1, 0.8, 3.6, 2.2, 6.5, 0.08, 0.9, 145.0, 95.0, 7.2, 36.0, 3.8, 14.2, 22.0, -7.8, 14.2, -10.5, 0.7190, 0.28, 0.78, 0.89),
    ("GEOFS006", "Banded_Iron_Formation", "iron_formation", "precambrian_ocean", 2400.0, "U238", "Pb206", 0.61, 0.639, 38.0, 2.5, 3.2, 0.1, 0.05, 2.8, 42.0, 0.25, 0.2, 1.0, 22.0, 0.5, 2.1, 1.8, 0.8, 7.6, -1.2, 12.5, -1.0, 0.7040, 0.92, 0.40, 0.86)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_geochemistry_history_model.csv")
open(outfile, "w") do io
    println(io, "sample_id,province,rock_type,parent_isotope,reported_age_ma,model_age_ma,CIA,mafic_index,crustal_evolution_proxy,redox_state_proxy,geochemical_history_pressure")
    for r in records
        sample_id = r[1]
        province = r[2]
        rock_type = r[3]
        parent = r[6]
        reported_age = r[5]
        parent_fraction = r[8]
        half_life = isotope_half_life_ma(parent)
        model_age = model_age_from_parent_fraction(parent_fraction, half_life)
        cia = chemical_index_of_alteration(r[11], r[12], r[13], r[14])
        mafic = mafic_index(r[15], r[16], r[18], r[10])
        crustal = crustal_evolution_proxy(r[10], r[19], r[20], r[28], r[29])
        redox_state = redox_state_proxy(r[30], r[16], r[17])
        pressure = geochemical_history_pressure(r)
        println(io, "$sample_id,$province,$rock_type,$parent,$reported_age,$model_age,$cia,$mafic,$crustal,$redox_state,$pressure")
    end
end

println("Julia geochemistry history model complete: $outfile")
