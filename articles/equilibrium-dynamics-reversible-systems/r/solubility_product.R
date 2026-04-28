# Solubility product comparison using simplified educational data.

solubility <- read.csv(file.path("data", "solubility_cases.csv"))

solubility$ion_product <- (
  solubility$cation_concentration_mol_l ^ solubility$cation_power
) * (
  solubility$anion_concentration_mol_l ^ solubility$anion_power
)

solubility$ion_product_over_Ksp <- solubility$ion_product / solubility$Ksp

solubility$interpretation <- ifelse(
  solubility$ion_product > solubility$Ksp,
  "supersaturated or precipitation favored",
  ifelse(
    solubility$ion_product < solubility$Ksp,
    "undersaturated or dissolution favored",
    "at saturation equilibrium"
  )
)

print(solubility)
