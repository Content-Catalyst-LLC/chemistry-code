program analytical_kernel
  implicit none

  real(8) :: concentration, detection_limit, quantification_limit
  real(8) :: resolution, beer_c

  concentration = (3.72d0 - 0.04d0) / 0.515d0
  detection_limit = 3.0d0 * 0.0032d0 / 0.515d0
  quantification_limit = 10.0d0 * 0.0032d0 / 0.515d0
  resolution = 2.0d0 * (5.20d0 - 3.10d0) / (0.42d0 + 0.50d0)
  beer_c = 0.625d0 / (12500.0d0 * 1.0d0)

  print *, "unknown_concentration=", concentration
  print *, "LOD=", detection_limit
  print *, "LOQ=", quantification_limit
  print *, "resolution=", resolution
  print *, "beer_lambert_c=", beer_c

end program analytical_kernel
