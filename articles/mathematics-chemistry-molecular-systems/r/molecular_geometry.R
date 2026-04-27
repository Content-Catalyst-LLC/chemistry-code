# Pairwise molecular distances from synthetic coordinate data.

coords <- read.csv(file.path("data", "molecular_coordinates.csv"))

distance_rows <- data.frame()

for (molecule in unique(coords$molecule)) {
  subset <- coords[coords$molecule == molecule, ]
  for (i in 1:(nrow(subset) - 1)) {
    for (j in (i + 1):nrow(subset)) {
      dx <- subset$x_angstrom[i] - subset$x_angstrom[j]
      dy <- subset$y_angstrom[i] - subset$y_angstrom[j]
      dz <- subset$z_angstrom[i] - subset$z_angstrom[j]
      distance <- sqrt(dx^2 + dy^2 + dz^2)

      distance_rows <- rbind(
        distance_rows,
        data.frame(
          molecule = molecule,
          atom_i = subset$atom[i],
          atom_j = subset$atom[j],
          distance_angstrom = distance
        )
      )
    }
  }
}

print(round(distance_rows, 6))
