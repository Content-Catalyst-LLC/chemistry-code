# Langmuir adsorption and surface-rate scaffold.
# Synthetic educational data only.

surface <- read.csv(file.path("data", "adsorption_cases.csv"))

surface$theta_A <- (surface$K_A * surface$pressure) /
  (1 + surface$K_A * surface$pressure)

surface$theta_B <- (surface$K_B * surface$pressure) /
  (1 + surface$K_B * surface$pressure)

surface$surface_rate <- surface$k_surface * surface$theta_A * surface$theta_B

print(surface)
