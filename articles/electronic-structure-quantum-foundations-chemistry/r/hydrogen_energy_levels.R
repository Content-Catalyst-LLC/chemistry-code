# Hydrogen-like energy levels and transitions.
# Simplified educational calculation.

h <- 6.62607015e-34
c <- 299792458.0
ev_to_j <- 1.602176634e-19

levels <- data.frame(n = 1:6)
levels$energy_eV <- -13.6 / (levels$n^2)
levels$energy_J <- levels$energy_eV * ev_to_j

ground_energy <- levels$energy_J[levels$n == 1]

transitions <- data.frame(n_initial = 2:6)
transitions$transition <- paste0(transitions$n_initial, "_to_1")
transitions$initial_energy_J <- levels$energy_J[match(transitions$n_initial, levels$n)]
transitions$delta_energy_J <- abs(transitions$initial_energy_J - ground_energy)
transitions$wavelength_nm <- (h * c / transitions$delta_energy_J) * 1e9

print(levels)
print(transitions[, c("transition", "delta_energy_J", "wavelength_nm")])
