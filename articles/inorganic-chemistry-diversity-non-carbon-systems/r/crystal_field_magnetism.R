# Crystal-field and spin-only magnetic moment scaffold.
# Synthetic educational examples only.

cases <- read.csv(file.path("data", "crystal_field_cases.csv"))

cases$CFSE_delta_o_units <- (
  cases$t2g_electrons * -0.4 * cases$delta_o_units +
    cases$eg_electrons * 0.6 * cases$delta_o_units
)

cases$spin_only_magnetic_moment_BM <- sqrt(
  cases$unpaired_electrons * (cases$unpaired_electrons + 2)
)

cases$diamagnetic_hint <- as.integer(cases$unpaired_electrons == 0)

print(cases)
