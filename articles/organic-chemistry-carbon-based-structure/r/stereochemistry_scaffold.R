# Stereochemistry scaffold.
# Synthetic educational examples only.

stereo <- read.csv(file.path("data", "stereochemistry_cases.csv"))

stereo$stereochemical_complexity_score <- with(
  stereo,
  stereocenters + double_bond_stereo_centers + chiral
)

print(stereo)
