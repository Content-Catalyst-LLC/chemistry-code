# Analytical chemistry numerical kernel in Julia.

function concentration_from_calibration(signal, slope, intercept)
    return (signal - intercept) / slope
end

function lod(blank_sd, slope)
    return 3.0 * blank_sd / slope
end

function loq(blank_sd, slope)
    return 10.0 * blank_sd / slope
end

function chromatographic_resolution(tR1, tR2, w1, w2)
    return 2.0 * (tR2 - tR1) / (w1 + w2)
end

function beer_lambert_concentration(absorbance, epsilon, path_length)
    return absorbance / (epsilon * path_length)
end

println("unknown_concentration=", round(concentration_from_calibration(3.72, 0.515, 0.04), digits=6))
println("LOD=", round(lod(0.0032, 0.515), digits=6))
println("LOQ=", round(loq(0.0032, 0.515), digits=6))
println("resolution=", round(chromatographic_resolution(3.10, 5.20, 0.42, 0.50), digits=6))
println("beer_lambert_c=", beer_lambert_concentration(0.625, 12500.0, 1.0))
