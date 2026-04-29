# Molecular descriptor scaffold.
# Synthetic educational examples only.

descriptors <- read.csv(file.path("data", "descriptors.csv"))

descriptors$hetero_atom_fraction <- descriptors$hetero_atoms / descriptors$heavy_atoms
descriptors$polarity_score <- descriptors$h_bond_donors + descriptors$h_bond_acceptors
descriptors$flexibility_score <- descriptors$rotatable_bonds / descriptors$heavy_atoms
descriptors$ring_density <- descriptors$rings / descriptors$heavy_atoms

print(descriptors)
