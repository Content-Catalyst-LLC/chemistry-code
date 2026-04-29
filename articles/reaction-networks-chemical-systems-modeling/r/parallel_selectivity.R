# Parallel pathway selectivity for A -> B and A -> C.
# Synthetic educational data only.

cases <- read.csv(file.path("data", "parallel_cases.csv"))

cases$fraction_to_B <- cases$k_to_B / (cases$k_to_B + cases$k_to_C)
cases$fraction_to_C <- cases$k_to_C / (cases$k_to_B + cases$k_to_C)
cases$B_to_C_selectivity <- cases$fraction_to_B / cases$fraction_to_C

print(cases)
