# One-dimensional diffusion scaffold.
# Educational finite-difference example only.

n <- 21
dx <- 1.0
dt <- 0.05
D <- 0.5

c <- rep(0, n)
c[ceiling(n / 2)] <- 1.0

for (step in 1:20) {
  c_new <- c

  for (i in 2:(n - 1)) {
    c_new[i] <- c[i] + D * dt / dx^2 * (c[i + 1] - 2 * c[i] + c[i - 1])
  }

  c <- c_new
}

diffusion_profile <- data.frame(
  position = 1:n,
  concentration = c
)

print(diffusion_profile)
