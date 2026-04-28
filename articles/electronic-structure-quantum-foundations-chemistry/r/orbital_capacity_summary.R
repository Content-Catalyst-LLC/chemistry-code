# Orbital capacity summary.

orbitals <- read.csv(file.path("data", "orbitals_sample.csv"))

orbitals$orbital_count <- 2 * orbitals$l + 1
orbitals$maximum_electrons <- 2 * orbitals$orbital_count

configs <- read.csv(file.path("data", "electron_configurations_sample.csv"))

print(orbitals)
print(configs)
