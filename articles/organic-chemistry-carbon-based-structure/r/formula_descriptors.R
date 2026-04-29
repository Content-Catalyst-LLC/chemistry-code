# Formula descriptors and degree of unsaturation.
# Synthetic educational examples only.

molecules <- read.csv(file.path("data", "molecular_formulas.csv"))

molecules$DBE <- molecules$C - (molecules$H + molecules$X) / 2 + molecules$N / 2 + 1
molecules$heteroatom_count <- molecules$N + molecules$O + molecules$S + molecules$X
molecules$heavy_atom_count <- molecules$C + molecules$N + molecules$O + molecules$S + molecules$X

print(molecules)
