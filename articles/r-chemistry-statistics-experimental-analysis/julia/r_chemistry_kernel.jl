# R chemistry numerical kernel in Julia.
# Mirrors simple statistical chemistry calculations.

function mean_value(x)
    return sum(x) / length(x)
end

function sample_sd(x)
    xbar = mean_value(x)
    return sqrt(sum((x .- xbar).^2) / (length(x) - 1))
end

function standard_error(x)
    return sample_sd(x) / sqrt(length(x))
end

function rsd_percent(x)
    return 100.0 * sample_sd(x) / mean_value(x)
end

function unknown_concentration(response, slope, intercept)
    return (response - intercept) / slope
end

values = [1.02, 1.05, 0.99]

println("mean=", round(mean_value(values), digits=6))
println("sample_sd=", round(sample_sd(values), digits=6))
println("standard_error=", round(standard_error(values), digits=6))
println("rsd_percent=", round(rsd_percent(values), digits=6))
println("unknown_concentration=", round(unknown_concentration(0.95, 0.30, 0.02), digits=6))
