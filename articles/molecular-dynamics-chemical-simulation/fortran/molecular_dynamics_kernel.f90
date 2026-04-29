program molecular_dynamics_kernel
  implicit none

  real(8) :: dt, r, v, a, r_new, v_new
  real(8) :: ratio, lj_energy, diffusion_estimate

  dt = 0.5d0
  r = 0.0d0
  v = 0.05d0
  a = 0.10d0

  r_new = r + v * dt + 0.5d0 * a * dt ** 2
  v_new = v + a * dt

  ratio = 1.0d0 / 1.12d0
  lj_energy = 4.0d0 * 1.0d0 * (ratio ** 12 - ratio ** 6)

  diffusion_estimate = 4.21d0 / (6.0d0 * 7.0d0)

  print *, "new_position=", r_new
  print *, "new_velocity=", v_new
  print *, "lj_energy=", lj_energy
  print *, "diffusion_estimate=", diffusion_estimate

end program molecular_dynamics_kernel
