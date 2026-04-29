# Two-level orbital mixing scaffold.
# Synthetic educational examples only.

cases <- read.csv(file.path("data", "orbital_mixing_cases.csv"))

rows <- data.frame()

for (i in seq_len(nrow(cases))) {
  row <- cases[i, ]

  H <- matrix(
    c(row$energy_a, row$coupling, row$coupling, row$energy_b),
    nrow = 2,
    byrow = TRUE
  )

  eig <- eigen(H, symmetric = TRUE)

  temp <- data.frame(
    case_id = row$case_id,
    orbital = c("MO_1", "MO_2"),
    energy_units = eig$values,
    coefficient_basis_a = eig$vectors[1, ],
    coefficient_basis_b = eig$vectors[2, ]
  )

  rows <- rbind(rows, temp)
}

print(rows)
