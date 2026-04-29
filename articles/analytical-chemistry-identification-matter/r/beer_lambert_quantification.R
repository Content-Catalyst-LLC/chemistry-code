# Beer-Lambert quantification scaffold.
# Synthetic educational examples only.

cases <- read.csv(file.path("data", "beer_lambert_cases.csv"))

cases$concentration_mol_L <- cases$absorbance /
  (cases$epsilon_L_mol_cm * cases$path_length_cm)

print(cases)
