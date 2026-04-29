# Boltzmann population scaffold.
# Synthetic educational states only.

kB <- 1.380649e-23

states <- read.csv(file.path("data", "boltzmann_states.csv"))

T <- states$temperature_K[1]
weights <- exp(-states$energy_J / (kB * T))
states$population <- weights / sum(weights)

print(states)
