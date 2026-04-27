# Oxidation mass gain table using synthetic examples.

oxidation <- read.csv(file.path("data", "oxidation_mass_gain.csv"))

oxidation$oxide_mass_g <- oxidation$metal_mass_g + oxidation$oxygen_mass_g
oxidation$oxygen_mass_fraction <- oxidation$oxygen_mass_g / oxidation$oxide_mass_g
oxidation$mass_gain_percent <- 100 * oxidation$oxygen_mass_g / oxidation$metal_mass_g

print(round(oxidation, 4))
