# Small Hamiltonian-style eigenvalue problem.

matrices <- read.csv(file.path("data", "hamiltonian_matrices.csv"))

for (i in 1:nrow(matrices)) {
  row <- matrices[i, ]

  H <- matrix(
    c(
      row$h11, row$h12, row$h13,
      row$h21, row$h22, row$h23,
      row$h31, row$h32, row$h33
    ),
    nrow = 3,
    byrow = TRUE
  )

  solution <- eigen(H, symmetric = TRUE)

  print(row$matrix_name)
  print(H)
  print(solution$values)
}
