# Basis-set convergence scaffold.
# Synthetic educational examples only.

hartree_to_kj_mol <- 2625.49962
basis <- read.csv(file.path("data", "basis_convergence.csv"))

basis$relative_energy_kj_mol <- ave(
  basis$energy_hartree,
  basis$case_id,
  FUN = function(x) (x - min(x)) * hartree_to_kj_mol
)

print(basis)
