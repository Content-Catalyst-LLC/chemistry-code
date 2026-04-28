# Monoprotic acid speciation.
# Synthetic educational data only.

pKa <- 4.76
Ka <- 10^(-pKa)

pH_values <- seq(0, 14, by = 0.5)
H <- 10^(-pH_values)

alpha_HA <- H / (H + Ka)
alpha_A_minus <- Ka / (H + Ka)

speciation <- data.frame(
  pH = pH_values,
  alpha_HA = alpha_HA,
  alpha_A_minus = alpha_A_minus
)

print(head(speciation, 10))
print(speciation[which.min(abs(speciation$pH - pKa)), ])
