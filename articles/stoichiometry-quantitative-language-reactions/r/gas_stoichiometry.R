# Gas stoichiometry using PV = nRT.
# Synthetic educational data only.

R_l_atm <- 0.082057338

gas <- read.csv(file.path("data", "gas_stoichiometry_examples.csv"))

gas$gas_moles <- (gas$pressure_atm * gas$volume_l) / (R_l_atm * gas$temperature_k)
gas$target_moles <- gas$gas_moles * gas$coefficient_target / gas$coefficient_gas

print(gas)
