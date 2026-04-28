# Center of mass and molecular extent calculations.

coords <- read.csv(file.path("data", "molecular_coordinates.csv"))

molecules <- unique(coords$molecule)
rows <- data.frame()

for (molecule in molecules) {
  subset <- coords[coords$molecule == molecule, ]

  center_geometry <- colMeans(subset[, c("x_angstrom", "y_angstrom", "z_angstrom")])

  center_mass <- colSums(subset[, c("x_angstrom", "y_angstrom", "z_angstrom")] * subset$mass_u) /
    sum(subset$mass_u)

  rows <- rbind(
    rows,
    data.frame(
      molecule = molecule,
      center_geometry_x = center_geometry[1],
      center_geometry_y = center_geometry[2],
      center_geometry_z = center_geometry[3],
      center_mass_x = center_mass[1],
      center_mass_y = center_mass[2],
      center_mass_z = center_mass[3]
    )
  )
}

print(round(rows, 6))
