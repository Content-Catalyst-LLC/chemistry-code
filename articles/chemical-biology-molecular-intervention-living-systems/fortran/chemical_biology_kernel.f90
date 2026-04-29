program chemical_biology_kernel
  implicit none

  real(8) :: response, occupancy, engagement

  response = 0.05d0 + (1.0d0 - 0.05d0) / (1.0d0 + (1.5d0 / 1.0d0) ** 1.2d0)
  occupancy = 2.0d0 / (2.0d0 + 2.0d0)
  engagement = (100.0d0 - 55.0d0) / (100.0d0 - 20.0d0)

  print *, "response=", response
  print *, "occupancy=", occupancy
  print *, "target_engagement=", engagement

end program chemical_biology_kernel
