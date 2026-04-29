# Tanimoto similarity scaffold.
# Synthetic binary fingerprints only.

fingerprints <- read.csv(file.path("data", "fingerprints.csv"))
bit_cols <- grep("^bit_", names(fingerprints), value = TRUE)

rows <- data.frame()

for (i in 1:(nrow(fingerprints) - 1)) {
  for (j in (i + 1):nrow(fingerprints)) {
    a_bits <- as.integer(fingerprints[i, bit_cols])
    b_bits <- as.integer(fingerprints[j, bit_cols])

    a <- sum(a_bits == 1)
    b <- sum(b_bits == 1)
    c <- sum(a_bits == 1 & b_bits == 1)

    tanimoto <- c / (a + b - c)

    rows <- rbind(
      rows,
      data.frame(
        molecule_a = fingerprints$molecule[i],
        molecule_b = fingerprints$molecule[j],
        tanimoto = tanimoto
      )
    )
  }
}

print(rows)
