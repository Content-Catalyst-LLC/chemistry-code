# Bond polarity from electronegativity differences.
# Thresholds are educational heuristics, not universal rules.

bonds <- read.csv(file.path("data", "bond_polarity_sample.csv"))

bonds$delta_chi <- abs(bonds$chi_a - bonds$chi_b)

bonds$simplified_classification <- ifelse(
  bonds$delta_chi < 0.4,
  "weakly polar or nearly nonpolar covalent",
  ifelse(bonds$delta_chi < 1.7, "polar covalent", "strongly polar or ionic model useful")
)

print(bonds)
