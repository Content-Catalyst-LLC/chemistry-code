# Goldschmidt tolerance factor scaffold.
# Synthetic educational radii only.

perovskites <- read.csv(file.path("data", "perovskite_cases.csv"))

perovskites$tolerance_factor <- with(
  perovskites,
  (r_A + r_X) / (sqrt(2) * (r_B + r_X))
)

perovskites$near_cubic_hint <- as.integer(
  perovskites$tolerance_factor >= 0.9 &
    perovskites$tolerance_factor <= 1.05
)

print(perovskites)
