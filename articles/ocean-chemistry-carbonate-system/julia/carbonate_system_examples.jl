# Ocean carbonate chemistry educational calculations in Julia.
# Includes carbonate fractions, saturation state, and air-sea CO2 flux proxy.

using Printf

article_dir = abspath(joinpath(@__DIR__, ".."))
table_dir = joinpath(article_dir, "outputs", "tables")
mkpath(table_dir)

const K1 = 10.0^-6.0
const K2 = 10.0^-9.1
const KSP_ARAGONITE = 6.5e-7

function carbonate_fractions(pH)
    H = 10.0^(-pH)
    denom = H^2 + K1 * H + K1 * K2
    alpha0 = H^2 / denom
    alpha1 = K1 * H / denom
    alpha2 = K1 * K2 / denom
    return alpha0, alpha1, alpha2
end

function omega_aragonite(calcium_mmol_kg, carbonate_umol_kg)
    return (calcium_mmol_kg * 1.0e-3) * (carbonate_umol_kg * 1.0e-6) / KSP_ARAGONITE
end

function flux_proxy(pco2_water, pco2_air)
    return pco2_water - pco2_air
end

cases = [
    ("Open-Ocean-A", 8.10, 2050.0, 10.3, 410.0),
    ("Upwelling-B", 7.78, 2240.0, 10.1, 820.0),
    ("Estuary-D", 7.62, 2300.0, 8.4, 1150.0)
]

open(joinpath(table_dir, "julia_carbonate_examples.csv"), "w") do io
    println(io, "station,pH,DIC_umol_kg,carbonate_umol_kg,omega_aragonite_simplified,co2_flux_proxy_uatm")
    for (station, pH, dic, calcium, pco2) in cases
        _, _, alpha2 = carbonate_fractions(pH)
        carbonate = alpha2 * dic
        omega = omega_aragonite(calcium, carbonate)
        flux = flux_proxy(pco2, 420.0)
        println(io, "$(station),$(pH),$(dic),$(carbonate),$(omega),$(flux)")
    end
end

println("Julia ocean carbonate workflow complete.")
