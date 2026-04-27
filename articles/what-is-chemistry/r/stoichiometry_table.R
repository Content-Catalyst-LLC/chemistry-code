# Moles and molarity calculations for synthetic chemistry examples.

examples <- read.csv(file.path("data", "intro_chemistry_examples.csv"))

examples$moles <- examples$mass_g / examples$molar_mass_g_mol
examples$molarity_mol_l <- examples$moles / examples$volume_l

print(round(examples, 5))
