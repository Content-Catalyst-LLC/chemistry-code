# Coordination chemistry descriptor scaffold.
# Synthetic educational examples only.

complexes <- read.csv(file.path("data", "coordination_cases.csv"))

complexes$high_coordination <- as.integer(complexes$coordination_number >= 6)
complexes$low_coordination <- as.integer(complexes$coordination_number <= 2)

print(complexes)
