# Redox titration electron equivalence.
# Synthetic educational data only.

titrations <- read.csv(file.path("data", "redox_titration_cases.csv"))

titrations$titrant_moles_required <- (
  titrations$analyte_moles *
    titrations$electrons_donated_per_analyte
) / titrations$electrons_accepted_per_titrant

titrations$titrant_volume_l <- titrations$titrant_moles_required /
  titrations$titrant_concentration_mol_l

titrations$titrant_volume_ml <- titrations$titrant_volume_l * 1000

print(titrations)
