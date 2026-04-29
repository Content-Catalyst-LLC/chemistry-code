# Mean-squared displacement and diffusion scaffold.
# Synthetic educational examples only.

trajectory <- read.csv(file.path("data", "trajectory_positions.csv"))

x0 <- trajectory$x[1]
y0 <- trajectory$y[1]
z0 <- trajectory$z[1]

trajectory$msd <- (trajectory$x - x0)^2 +
  (trajectory$y - y0)^2 +
  (trajectory$z - z0)^2

trajectory$diffusion_estimate <- ifelse(
  trajectory$time_ps > 0,
  trajectory$msd / (6 * trajectory$time_ps),
  NA
)

print(trajectory)
