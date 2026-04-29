# Transition-state-theory scaffold.
# Synthetic educational examples only.

kB <- 1.380649e-23
h <- 6.62607015e-34
R <- 8.314462618

cases <- read.csv(file.path("data", "tst_cases.csv"))

cases$rate_s_inv <- with(
  cases,
  (kB * temperature_K / h) *
    exp(-(activation_free_energy_kj_mol * 1000) / (R * temperature_K))
)

cases$log10_rate <- log10(cases$rate_s_inv)

print(cases)
