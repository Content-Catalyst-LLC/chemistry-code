# Calculate selected bond distances from molecular coordinates.

coords <- read.csv(file.path("data", "molecular_coordinates.csv"))
bonds <- read.csv(file.path("data", "bonds_sample.csv"))

rows <- data.frame()

for (i in 1:nrow(bonds)) {
  bond <- bonds[i, ]
  subset <- coords[coords$molecule == bond$molecule, ]

  atom_i <- subset[subset$atom == bond$atom_i, ]
  atom_j <- subset[subset$atom == bond$atom_j, ]

  dx <- atom_i$x_angstrom - atom_j$x_angstrom
  dy <- atom_i$y_angstrom - atom_j$y_angstrom
  dz <- atom_i$z_angstrom - atom_j$z_angstrom

  rows <- rbind(
    rows,
    data.frame(
      molecule = bond$molecule,
      atom_i = bond$atom_i,
      atom_j = bond$atom_j,
      distance_angstrom = sqrt(dx^2 + dy^2 + dz^2)
    )
  )
}

print(round(rows, 6))
