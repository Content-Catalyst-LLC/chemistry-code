# Python chemistry numerical kernel in Julia.
# This mirrors simple calculations used in Python-centered chemistry workflows.

function unknown_concentration(response, slope, intercept)
    return (response - intercept) / slope
end

function first_order_concentration(c0, k, t)
    return c0 * exp(-k * t)
end

function half_life_first_order(k)
    return log(2.0) / k
end

function standard_error(sd, n)
    return sd / sqrt(n)
end

println("unknown_concentration_mM=", round(unknown_concentration(0.95, 0.30, 0.02), digits=6))
println("first_order_concentration_mM=", round(first_order_concentration(10.0, 0.015, 100.0), digits=6))
println("half_life_s=", round(half_life_first_order(0.015), digits=6))
println("standard_error=", round(standard_error(0.03, 3), digits=6))
