# Synthetic interlaboratory comparison using normalized error.

comparison <- read.csv(file.path("data", "interlaboratory_comparison.csv"))

comparison$bias <- comparison$lab_result - comparison$reference_value
comparison$normalized_error_en <- comparison$bias / sqrt(
  comparison$lab_expanded_uncertainty^2 + comparison$reference_expanded_uncertainty^2
)
comparison$acceptable_by_abs_en_le_1 <- abs(comparison$normalized_error_en) <= 1

print(round(comparison, 4))
