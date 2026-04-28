# Nernst equation under nonstandard conditions.
# Synthetic educational data only.

R_const <- 8.314462618
F_const <- 96485.33212

cases <- read.csv(file.path("data", "nernst_cases.csv"))

cases$E_V <- cases$E_standard_V - (
  R_const * cases$temperature_K /
    (cases$electrons_transferred * F_const)
) * log(cases$reaction_quotient)

cases$potential_shift_V <- cases$E_V - cases$E_standard_V

print(cases)
