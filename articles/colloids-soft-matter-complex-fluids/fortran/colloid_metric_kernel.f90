program colloid_metric_kernel
  implicit none

  real(8) :: kB, T, eta0, diameter_nm, diameter_m, diffusion
  real(8) :: phi, relative_viscosity

  kB = 1.380649d-23
  T = 298.15d0
  eta0 = 0.00089d0

  diameter_nm = 80.0d0
  diameter_m = diameter_nm * 1.0d-9
  phi = 0.04d0

  diffusion = kB * T / (3.0d0 * 3.141592653589793d0 * eta0 * diameter_m)
  relative_viscosity = 1.0d0 + 2.5d0 * phi

  print *, "Colloid metric kernel"
  print *, "Diffusion estimate m^2/s:", diffusion
  print *, "Einstein relative viscosity:", relative_viscosity
  print *, "Responsible-use note: synthetic educational calculation only."
end program colloid_metric_kernel
