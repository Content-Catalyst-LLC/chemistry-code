# Green Chemistry, Responsibility, and Sustainable Transformation
# Julia green chemistry metrics and route scoring.
# Synthetic educational code only.

function clamp01(x)
    return max(0.0, min(1.0, x))
end

function atom_economy(product_mw, reactant_mw_sum)
    reactant_mw_sum <= 0 ? 0.0 : product_mw / reactant_mw_sum
end

function e_factor(waste_mass, product_mass)
    product_mass <= 0 ? 0.0 : waste_mass / product_mass
end

function pmi(total_input_mass, product_mass)
    product_mass <= 0 ? 0.0 : total_input_mass / product_mass
end

function solvent_burden(solvent_mass, product_mass)
    product_mass <= 0 ? 0.0 : solvent_mass / product_mass
end

function energy_intensity(energy_kwh, product_mass)
    product_mass <= 0 ? 0.0 : energy_kwh / product_mass
end

function catalysis_score(catalyst_loading)
    catalyst_loading <= 0 ? 0.0 : clamp01(1.0 - catalyst_loading / 20.0)
end

function process_safety_score(temp_c, pressure_bar, accident_potential, monitoring)
    condition_pressure = 0.5 * clamp01((temp_c - 25.0) / 175.0) + 0.5 * clamp01((pressure_bar - 1.0) / 20.0)
    return clamp01(0.45 * (1.0 - accident_potential) + 0.35 * monitoring + 0.20 * (1.0 - condition_pressure))
end

function green_score(row)
    route, product_mass, product_mw, reactant_sum, total_input, waste, solvent, energy, temp, pressure, catalyst, hazard, solvent_hazard, renewable, circularity, degradation, accident, monitoring = row

    ae = clamp01(atom_economy(product_mw, reactant_sum))
    waste_score = clamp01(1.0 - e_factor(waste, product_mass) / 25.0)
    pmi_score = clamp01(1.0 - pmi(total_input, product_mass) / 30.0)
    hazard_score = clamp01(1.0 - hazard)
    solvent_score = clamp01(1.0 - solvent_hazard)
    energy_score = clamp01(1.0 - energy_intensity(energy, product_mass) / 60.0)
    cat = catalysis_score(catalyst)
    circular = 0.5 * circularity + 0.5 * degradation
    safety = process_safety_score(temp, pressure, accident, monitoring)

    return clamp01(0.14 * ae + 0.14 * waste_score + 0.12 * pmi_score + 0.13 * hazard_score + 0.10 * solvent_score + 0.09 * energy_score + 0.08 * cat + 0.08 * renewable + 0.08 * circular + 0.04 * safety)
end

routes = [
    ("Route_A_Stoichiometric", 2.0, 180.0, 260.0, 36.0, 28.0, 22.0, 95.0, 85.0, 1.0, 0.0, 0.55, 0.62, 0.20, 0.30, 0.25, 0.35, 0.20),
    ("Route_B_Catalytic", 2.4, 180.0, 225.0, 18.0, 10.0, 9.0, 42.0, 45.0, 1.0, 2.0, 0.30, 0.35, 0.55, 0.62, 0.58, 0.18, 0.70),
    ("Route_F_Flow_Chemistry", 4.0, 320.0, 390.0, 28.0, 12.0, 8.0, 35.0, 60.0, 8.0, 1.0, 0.26, 0.28, 0.40, 0.70, 0.50, 0.16, 0.88)
]

root = abspath(joinpath(@__DIR__, ".."))
outdir = joinpath(root, "outputs", "tables")
mkpath(outdir)

outfile = joinpath(outdir, "julia_green_chemistry_scores.csv")
open(outfile, "w") do io
    println(io, "route,atom_economy,e_factor,pmi,solvent_burden,energy_intensity,green_score")
    for r in routes
        route = r[1]
        println(io, "$route,$(atom_economy(r[3],r[4])),$(e_factor(r[6],r[2])),$(pmi(r[5],r[2])),$(solvent_burden(r[7],r[2])),$(energy_intensity(r[8],r[2])),$(green_score(r))")
    end
end

println("Julia green chemistry model complete: $outfile")
