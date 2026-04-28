# Coefficient-aware titration equivalence.
# C_analyte V_analyte / a = C_titrant V_titrant / b

titrations <- read.csv(file.path("data", "titration_examples.csv"))

titrations$analyte_concentration_mol_l <- (
  titrations$analyte_coefficient *
    titrations$titrant_concentration_mol_l *
    titrations$titrant_volume_l
) / (
  titrations$titrant_coefficient *
    titrations$analyte_volume_l
)

print(titrations)
