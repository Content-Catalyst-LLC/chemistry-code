# Formal charge and simple molecular-orbital bond order.

formal <- read.csv(file.path("data", "formal_charge_examples.csv"))
formal$formal_charge <- formal$valence_electrons -
  formal$nonbonding_electrons -
  formal$bonding_electrons / 2

mo <- read.csv(file.path("data", "mo_bond_order_examples.csv"))
mo$bond_order <- (mo$bonding_electrons - mo$antibonding_electrons) / 2

print(formal)
print(mo)
