# Oxidation-state accounting scaffold.
# Synthetic educational examples only.

cases <- read.csv(file.path("data", "oxidation_state_cases.csv"))

cases$unknown_oxidation_state <- (
  cases$total_charge - cases$known_contribution
) / cases$unknown_atom_count

cases$charge_balance_check <- (
  cases$known_contribution +
    cases$unknown_atom_count * cases$unknown_oxidation_state
)

print(cases)
