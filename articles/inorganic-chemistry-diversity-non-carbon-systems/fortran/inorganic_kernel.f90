program inorganic_kernel
  implicit none

  real(8) :: mn_os, d3_cfse, spin_moment, tolerance

  mn_os = (0.0d0 - (-7.0d0)) / 1.0d0
  d3_cfse = 3.0d0 * (-0.4d0 * 1.0d0) + 0.0d0 * (0.6d0 * 1.0d0)
  spin_moment = sqrt(3.0d0 * (3.0d0 + 2.0d0))
  tolerance = (1.60d0 + 1.40d0) / (sqrt(2.0d0) * (0.60d0 + 1.40d0))

  print *, "Mn_in_KMnO4_OS=", mn_os
  print *, "octahedral_d3_CFSE=", d3_cfse
  print *, "spin_only_d3=", spin_moment
  print *, "tolerance_factor=", tolerance

end program inorganic_kernel
