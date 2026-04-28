# Periodic classification numerical kernel in Julia.

function isotope_weighted_mass(masses, abundances)
    return sum(masses .* abundances)
end

function neutron_number(mass_number, atomic_number)
    return mass_number - atomic_number
end

function feature_distance(a, b)
    return sqrt(sum((a .- b).^2))
end

cl_mass = isotope_weighted_mass([34.96885268, 36.96590260], [0.7576, 0.2424])
c13_neutrons = neutron_number(13, 6)
li_na_distance = feature_distance([1.0, 2.0, 128.0, 520.0], [1.0, 3.0, 166.0, 496.0])

println("chlorine_weighted_atomic_mass_u=", round(cl_mass, digits=6))
println("carbon_13_neutron_number=", c13_neutrons)
println("li_na_feature_distance_unscaled=", round(li_na_distance, digits=6))
