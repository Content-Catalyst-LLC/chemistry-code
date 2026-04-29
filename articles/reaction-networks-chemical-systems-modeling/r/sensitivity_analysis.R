# Finite-difference sensitivity of final C to k1.
# Synthetic educational data only.

simulate_network <- function(k1, k2 = 0.08, k3 = 0.05, k4 = 0.03, dt = 0.25, total_time = 50) {
  A <- 1.0
  B <- 0.0
  C <- 0.0
  D <- 0.0
  E <- 0.0

  time <- seq(0, total_time, by = dt)

  for (t in time[-1]) {
    r1 <- k1 * A
    r2 <- k2 * B
    r3 <- k3 * A
    r4 <- k4 * B

    A <- max(A + (-r1 - r3) * dt, 0)
    B <- max(B + (r1 - r2 - r4) * dt, 0)
    C <- max(C + r2 * dt, 0)
    D <- max(D + r3 * dt, 0)
    E <- max(E + r4 * dt, 0)
  }

  return(C)
}

base_k1 <- 0.20
delta <- 0.01

C_low <- simulate_network(base_k1 - delta)
C_high <- simulate_network(base_k1 + delta)
sensitivity <- (C_high - C_low) / (2 * delta)

print(paste("Final C at k1-delta:", round(C_low, 6)))
print(paste("Final C at k1+delta:", round(C_high, 6)))
print(paste("Sensitivity:", round(sensitivity, 6)))
