# Isotope-weighted atomic mass using simplified educational data.

isotopes <- read.csv(file.path("data", "isotopes_sample.csv"))

isotopes$neutron_number <- isotopes$mass_number - isotopes$atomic_number
isotopes$weighted_contribution_u <- isotopes$isotopic_mass_u * isotopes$fractional_abundance

weighted <- aggregate(
  weighted_contribution_u ~ element_symbol,
  data = isotopes,
  FUN = sum
)

names(weighted)[2] <- "weighted_atomic_mass_u"

print(isotopes)
print(weighted)
