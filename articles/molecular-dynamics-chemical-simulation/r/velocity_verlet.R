# Velocity Verlet scaffold.
# Synthetic educational examples only.

dt <- 0.5
particles <- read.csv(file.path("data", "particles_initial.csv"))

particles$acceleration <- particles$force / particles$mass
particles$new_position <- particles$position +
  particles$velocity * dt +
  0.5 * particles$acceleration * dt^2
particles$new_velocity <- particles$velocity + particles$acceleration * dt
particles$kinetic_energy_initial <- 0.5 * particles$mass * particles$velocity^2
particles$kinetic_energy_updated <- 0.5 * particles$mass * particles$new_velocity^2

print(particles)
