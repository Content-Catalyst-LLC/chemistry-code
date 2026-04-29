# Lennard-Jones potential scaffold.
# Synthetic educational examples only.

data <- read.csv(file.path("data", "lennard_jones_cases.csv"))

ratio <- data$sigma / data$distance
data$lj_energy <- 4 * data$epsilon * (ratio^12 - ratio^6)

print(data)
