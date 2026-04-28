# Dynamic approach to equilibrium for A reversible B.
# Euler integration is used for educational transparency.

cases <- read.csv(file.path("data", "reversible_dynamics_cases.csv"))

for (row_index in seq_len(nrow(cases))) {
  case <- cases[row_index, ]

  time <- seq(0, case$total_time_min, by = case$time_step_min)
  dt <- case$time_step_min

  A <- numeric(length(time))
  B <- numeric(length(time))
  Q <- numeric(length(time))

  A[1] <- case$A0_mol_l
  B[1] <- case$B0_mol_l
  Q[1] <- ifelse(A[1] > 0, B[1] / A[1], Inf)

  for (i in 2:length(time)) {
    forward_rate <- case$kf_per_min * A[i - 1]
    reverse_rate <- case$kr_per_min * B[i - 1]
    net_rate <- forward_rate - reverse_rate

    A[i] <- max(A[i - 1] - net_rate * dt, 0)
    B[i] <- max(B[i - 1] + net_rate * dt, 0)
    Q[i] <- ifelse(A[i] > 0, B[i] / A[i], Inf)
  }

  trajectory <- data.frame(
    case_id = case$case_id,
    time_min = time,
    A_mol_l = A,
    B_mol_l = B,
    Q = Q,
    expected_K = case$kf_per_min / case$kr_per_min
  )

  print(head(trajectory, 12))
  print(tail(trajectory, 6))
}
