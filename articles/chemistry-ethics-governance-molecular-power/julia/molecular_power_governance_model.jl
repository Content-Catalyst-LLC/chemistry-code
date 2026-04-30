# Chemistry, Ethics, and the Governance of Molecular Power
# Julia molecular power governance model.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function chemical_risk(hazard, exposure, vulnerability, persistence, irreversibility)
    baseline = hazard * exposure * vulnerability
    durability = 0.5 * persistence + 0.5 * irreversibility
    return clamp01(0.72 * baseline + 0.28 * durability)
end

function justice_weighted_risk(risk, inequality, worker)
    return clamp01(risk * (1.0 + 0.50 * inequality + 0.35 * worker))
end

function governance_gap(jrisk, governance)
    return clamp01(jrisk * (1.0 - governance))
end

function transparency_confidence(transparency, data, monitoring, qc)
    return clamp01(0.40 * transparency + 0.30 * data + 0.20 * monitoring + 0.10 * qc)
end

function stewardship_capacity(stewardship, governance, monitoring, alternatives)
    return clamp01(0.35 * stewardship + 0.25 * governance + 0.20 * monitoring + 0.20 * alternatives)
end

function responsible_score(row)
    domain, context, benefit, hazard, exposure, vulnerability, persistence, irreversibility, inequality, worker, dual, transparency, monitoring, alternatives, stewardship, governance, data, qc = row

    risk = chemical_risk(hazard, exposure, vulnerability, persistence, irreversibility)
    jrisk = justice_weighted_risk(risk, inequality, worker)
    gap = governance_gap(jrisk, governance)
    trans = transparency_confidence(transparency, data, monitoring, qc)
    steward = stewardship_capacity(stewardship, governance, monitoring, alternatives)

    return clamp01(0.26 * benefit + 0.22 * steward + 0.16 * trans + 0.12 * alternatives - 0.14 * jrisk - 0.06 * dual - 0.04 * gap)
end

records = [
    ("medicine", "essential_therapeutic", 0.95, 0.35, 0.42, 0.55, 0.30, 0.25, 0.22, 0.30, 0.05, 0.78, 0.72, 0.45, 0.80, 0.82, 0.88, 0.94),
    ("agriculture", "high_volume_pesticide", 0.72, 0.68, 0.76, 0.84, 0.62, 0.50, 0.58, 0.72, 0.12, 0.45, 0.50, 0.62, 0.48, 0.55, 0.66, 0.89),
    ("dual_use", "restricted_toxic_precursor", 0.22, 0.92, 0.35, 0.88, 0.60, 0.90, 0.52, 0.68, 0.95, 0.22, 0.60, 0.80, 0.30, 0.88, 0.74, 0.90)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_molecular_power_governance_scores.csv")
open(outfile, "w") do io
    println(io, "domain,use_context,chemical_risk,justice_weighted_risk,governance_gap,transparency_confidence,stewardship_capacity,responsible_innovation_score")
    for r in records
        domain, context, benefit, hazard, exposure, vulnerability, persistence, irreversibility, inequality, worker, dual, transparency, monitoring, alternatives, stewardship, governance, data, qc = r
        risk = chemical_risk(hazard, exposure, vulnerability, persistence, irreversibility)
        jrisk = justice_weighted_risk(risk, inequality, worker)
        gap = governance_gap(jrisk, governance)
        trans = transparency_confidence(transparency, data, monitoring, qc)
        steward = stewardship_capacity(stewardship, governance, monitoring, alternatives)
        score = responsible_score(r)
        println(io, "$domain,$context,$risk,$jrisk,$gap,$trans,$steward,$score")
    end
end

println("Julia molecular power governance model complete: $outfile")
