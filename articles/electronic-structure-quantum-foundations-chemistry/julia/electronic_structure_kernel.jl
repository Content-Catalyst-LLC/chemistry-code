# Electronic structure numerical kernel in Julia.

const H = 6.62607015e-34
const C = 299792458.0
const EV_TO_J = 1.602176634e-19
const ELECTRON_MASS = 9.1093837139e-31

function hydrogen_energy_ev(n)
    return -13.6 / n^2
end

function photon_wavelength_nm(delta_energy_ev)
    delta_j = delta_energy_ev * EV_TO_J
    return (H * C / delta_j) * 1.0e9
end

function particle_in_box_energy_ev(n, box_length_nm)
    length_m = box_length_nm * 1.0e-9
    energy_j = (n^2 * H^2) / (8.0 * ELECTRON_MASS * length_m^2)
    return energy_j / EV_TO_J
end

println("hydrogen_n1_energy_eV=", round(hydrogen_energy_ev(1), digits=6))
println("hydrogen_n2_energy_eV=", round(hydrogen_energy_ev(2), digits=6))
println("n2_to_n1_wavelength_nm=", round(photon_wavelength_nm(abs(hydrogen_energy_ev(2) - hydrogen_energy_ev(1))), digits=3))
println("particle_box_n1_1nm_eV=", round(particle_in_box_energy_ev(1, 1.0), digits=6))
