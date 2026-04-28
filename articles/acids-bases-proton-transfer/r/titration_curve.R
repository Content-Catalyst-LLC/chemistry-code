# Strong acid-strong base titration scaffold.
# Synthetic educational data only.

acid_concentration <- 0.100
acid_volume_l <- 0.025
base_concentration <- 0.100

base_volume_l <- seq(0, 0.050, by = 0.001)

acid_moles_initial <- acid_concentration * acid_volume_l
results <- data.frame()

for (vb in base_volume_l) {
  base_moles <- base_concentration * vb
  total_volume <- acid_volume_l + vb

  if (base_moles < acid_moles_initial) {
    h <- (acid_moles_initial - base_moles) / total_volume
    pH <- -log10(h)
  } else if (base_moles > acid_moles_initial) {
    oh <- (base_moles - acid_moles_initial) / total_volume
    pH <- 14 + log10(oh)
  } else {
    pH <- 7
  }

  results <- rbind(results, data.frame(base_volume_ml = vb * 1000, pH = pH))
}

print(head(results, 10))
print(results[results$base_volume_ml %in% c(24, 25, 26), ])
