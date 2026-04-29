# Reaction network simulation for A -> B -> C with side pathways.
# Euler integration is used for educational transparency.

dt <- 0.25
time <- seq(0, 50, by = dt)

k1 <- 0.20
k2 <- 0.08
k3 <- 0.05
k4 <- 0.03

A <- 1.0
B <- 0.0
C <- 0.0
D <- 0.0
E <- 0.0

rows <- data.frame()

for (t in time) {
  rows <- rbind(rows, data.frame(time = t, A = A, B = B, C = C, D = D, E = E))

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

print(head(rows, 12))
print(tail(rows, 6))
