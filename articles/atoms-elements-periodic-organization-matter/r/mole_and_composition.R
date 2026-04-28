# Mole conversion and percent composition examples.

avogadro_constant <- 6.02214076e23

mole_examples <- read.csv(file.path("data", "mole_examples.csv"))
mole_examples$amount_mol <- mole_examples$mass_g / mole_examples$molar_mass_g_mol
mole_examples$estimated_entities <- mole_examples$amount_mol * avogadro_constant

compounds <- read.csv(file.path("data", "compounds_sample.csv"))
compounds$element_mass_contribution <- compounds$atom_count * compounds$atomic_mass_u

compound_totals <- aggregate(
  element_mass_contribution ~ compound,
  data = compounds,
  FUN = sum
)

names(compound_totals)[2] <- "compound_molar_mass"

composition <- merge(compounds, compound_totals, by = "compound")
composition$percent_by_mass <- composition$element_mass_contribution / composition$compound_molar_mass * 100

print(mole_examples)
print(composition)
