# Functional group descriptor scaffold.
# Synthetic educational examples only.

groups <- read.csv(file.path("data", "functional_group_cases.csv"))

group_columns <- setdiff(names(groups), "molecule")
groups$functional_group_count <- rowSums(groups[, group_columns])

polar_columns <- c(
  "alcohol", "ether", "amine", "aldehyde", "ketone",
  "carboxylic_acid", "ester", "amide", "nitrile", "thiol", "sulfide"
)

groups$has_polar_group <- as.integer(rowSums(groups[, polar_columns]) > 0)

print(groups)
