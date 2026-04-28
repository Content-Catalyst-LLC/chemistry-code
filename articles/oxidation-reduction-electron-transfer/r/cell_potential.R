# Cell potential and Gibbs free energy.
# Synthetic educational data only.

F_const <- 96485.33212

cells <- read.csv(file.path("data", "cell_potential_cases.csv"))

cells$E_cell_standard_V <- cells$E_cathode_V - cells$E_anode_V
cells$delta_g_standard_kj_mol <- (
  -cells$electrons_transferred * F_const * cells$E_cell_standard_V / 1000
)

print(cells)
