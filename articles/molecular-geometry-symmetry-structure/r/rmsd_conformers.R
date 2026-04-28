# RMSD between simplified conformers.

conformers <- read.csv(file.path("data", "conformer_coordinates.csv"))

a <- conformers[conformers$conformer == "A", ]
b <- conformers[conformers$conformer == "B", ]

a <- a[order(a$atom), ]
b <- b[order(b$atom), ]

coords_a <- as.matrix(a[, c("x_angstrom", "y_angstrom", "z_angstrom")])
coords_b <- as.matrix(b[, c("x_angstrom", "y_angstrom", "z_angstrom")])

rmsd <- sqrt(mean(rowSums((coords_a - coords_b)^2)))

print(paste("RMSD:", round(rmsd, 6), "angstrom"))
