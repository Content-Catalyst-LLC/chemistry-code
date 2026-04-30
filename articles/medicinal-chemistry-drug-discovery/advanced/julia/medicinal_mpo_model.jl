# Medicinal Chemistry and Drug Discovery
# Julia multiparameter optimization model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function pic50_from_nm(ic50_nm)
    return -log10(ic50_nm * 1e-9)
end

function lle(ic50_nm, clogp)
    return pic50_from_nm(ic50_nm) - clogp
end

function selectivity_window(off_target_ic50_nm, target_ic50_nm)
    if target_ic50_nm <= 0
        return 0.0
    end
    return off_target_ic50_nm / target_ic50_nm
end

function safety_liability(herg_ic50_um, cyp3a4_ic50_um, alert_count, aromatic_rings)
    herg_risk = clamp01((10.0 - herg_ic50_um) / 10.0)
    cyp_risk = clamp01((20.0 - cyp3a4_ic50_um) / 20.0)
    alert_risk = clamp01(alert_count / 3.0)
    aromatic_risk = clamp01((aromatic_rings - 3.0) / 3.0)

    return clamp01(
        0.38 * herg_risk +
        0.28 * cyp_risk +
        0.22 * alert_risk +
        0.12 * aromatic_risk
    )
end

function oral_property_score(mw, clogp, tpsa, hbd, hba, rot_bonds, solubility_um, permeability)
    lipinski_penalty =
        (mw > 500 ? 1 : 0) +
        (clogp > 5 ? 1 : 0) +
        (hbd > 5 ? 1 : 0) +
        (hba > 10 ? 1 : 0)

    veber_penalty =
        (tpsa > 140 ? 1 : 0) +
        (rot_bonds > 10 ? 1 : 0)

    solubility_score = clamp01(log10(max(solubility_um, 0.001)) / 2.3)
    permeability_score = clamp01(permeability / 30.0)

    return clamp01(
        0.25 * (1.0 - lipinski_penalty / 4.0) +
        0.20 * (1.0 - veber_penalty / 2.0) +
        0.30 * solubility_score +
        0.25 * permeability_score
    )
end

function mpo_score(row)
    compound, ic50, off_target, herg, cyp, sol, perm, mw, clogp, tpsa, hbd, hba, rot, alerts, rings, qc = row

    potency = clamp01((pic50_from_nm(ic50) - 5.0) / 3.0)
    selectivity = clamp01(log10(max(selectivity_window(off_target, ic50), 1.0)) / 3.0)
    lle_score = clamp01((lle(ic50, clogp) - 2.0) / 5.0)
    property = oral_property_score(mw, clogp, tpsa, hbd, hba, rot, sol, perm)
    safety = 1.0 - safety_liability(herg, cyp, alerts, rings)

    return clamp01(
        0.24 * potency +
        0.18 * selectivity +
        0.18 * lle_score +
        0.18 * property +
        0.16 * safety +
        0.06 * qc
    )
end

compounds = [
    ("MEDADV001", 18.0, 2100.0, 18.0, 22.0, 45.0, 18.0, 438.0, 3.2, 78.0, 1.0, 7.0, 5.0, 0.0, 3.0, 0.94),
    ("MEDADV003", 7.0, 320.0, 4.0, 18.0, 65.0, 22.0, 392.0, 2.8, 62.0, 1.0, 6.0, 4.0, 0.0, 2.0, 0.92),
    ("MEDADV006", 32.0, 5200.0, 42.0, 55.0, 160.0, 26.0, 356.0, 1.9, 70.0, 2.0, 7.0, 3.0, 0.0, 1.0, 0.95),
    ("MEDADV008", 4.0, 4800.0, 25.0, 30.0, 34.0, 16.0, 488.0, 4.6, 105.0, 2.0, 8.0, 7.0, 1.0, 4.0, 0.91)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_medicinal_mpo_scores.csv")
open(outfile, "w") do io
    println(io, "compound_id,pIC50,LLE,selectivity_window,MPO_score")
    for row in compounds
        compound = row[1]
        ic50 = row[2]
        off_target = row[3]
        println(io, "$compound,$(pic50_from_nm(ic50)),$(lle(ic50,row[9])),$(selectivity_window(off_target,ic50)),$(mpo_score(row))")
    end
end

println("Julia medicinal MPO model complete: $outfile")
