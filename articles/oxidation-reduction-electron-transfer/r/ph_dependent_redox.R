# pH-dependent redox potential scaffold.
# Generic reaction: Ox + mH+ + ne- -> Red

R_const <- 8.314462618
F_const <- 96485.33212

case <- data.frame(
  E_standard_V = 1.23,
  electrons_transferred = 4,
  protons_transferred = 4,
  temperature_K = 298.15
)

pH <- seq(0, 14, by = 1)
H_activity <- 10^(-pH)
Q <- 1 / (H_activity ^ case$protons_transferred)

E <- case$E_standard_V - (
  R_const * case$temperature_K /
    (case$electrons_transferred * F_const)
) * log(Q)

profile <- data.frame(pH = pH, E_V = E)

print(profile)
