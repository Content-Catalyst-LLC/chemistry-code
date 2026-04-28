# Weak acid pH calculation using exact quadratic solution.
# Synthetic educational data only.

acids <- read.csv(file.path("data", "weak_acid_cases.csv"))

rows <- data.frame()

for (i in seq_len(nrow(acids))) {
  Ka <- acids$Ka[i]
  C <- acids$initial_concentration_mol_l[i]

  H <- (-Ka + sqrt(Ka^2 + 4 * Ka * C)) / 2
  pH <- -log10(H)
  percent_dissociation <- H / C * 100

  rows <- rbind(
    rows,
    data.frame(
      case_id = acids$case_id[i],
      acid = acids$acid[i],
      hydronium_mol_l = H,
      pH = pH,
      percent_dissociation = percent_dissociation
    )
  )
}

print(rows)
