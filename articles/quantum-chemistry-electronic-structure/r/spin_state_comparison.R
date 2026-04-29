# Spin-state comparison scaffold.
# Synthetic educational examples only.

spin <- read.csv(file.path("data", "spin_state_cases.csv"))

spin$ground_state_hint <- ave(
  spin$relative_energy_kj_mol,
  spin$complex,
  FUN = function(x) as.integer(x == min(x))
)

print(spin)
