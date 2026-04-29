program biochemistry_kernel
  implicit none

  real(8) :: velocity, occupancy, hill_occupancy, delta_g
  real(8), parameter :: R = 8.314462618d0

  velocity = 120.0d0 * 5.0d0 / (3.5d0 + 5.0d0)
  occupancy = 2.0d0 / (2.0d0 + 2.0d0)
  hill_occupancy = (2.0d0 ** 2.0d0) / ((2.0d0 ** 2.0d0) + (2.0d0 ** 2.0d0))
  delta_g = -(R * 298.15d0 * log(1000.0d0)) / 1000.0d0

  print *, "velocity=", velocity
  print *, "occupancy=", occupancy
  print *, "hill_occupancy=", hill_occupancy
  print *, "delta_g_kj_mol=", delta_g

end program biochemistry_kernel
