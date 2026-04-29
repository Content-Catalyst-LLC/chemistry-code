# Simple structure-property descriptor scaffold.
# Synthetic educational examples only.

organic_set <- read.csv(file.path("data", "structure_property_cases.csv"))

organic_set$polarity_score <- with(
  organic_set,
  heteroatom_count + hydrogen_bond_donors + hydrogen_bond_acceptors
)

organic_set$hydrophobic_skeleton_score <- organic_set$carbon_count + organic_set$ring_count

organic_set$complexity_score <- with(
  organic_set,
  carbon_count +
    2 * heteroatom_count +
    2 * ring_count +
    2 * aromatic_ring_count +
    3 * stereocenter_count
)

print(organic_set)
