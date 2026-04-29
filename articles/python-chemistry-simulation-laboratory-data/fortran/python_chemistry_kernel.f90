program python_chemistry_kernel
  implicit none

  real(8) :: response, slope, intercept, unknown
  real(8) :: c0, k, t, concentration, half_life
  real(8) :: sd, n, se

  response = 0.95d0
  slope = 0.30d0
  intercept = 0.02d0
  unknown = (response - intercept) / slope

  c0 = 10.0d0
  k = 0.015d0
  t = 100.0d0
  concentration = c0 * exp(-k * t)
  half_life = log(2.0d0) / k

  sd = 0.03d0
  n = 3.0d0
  se = sd / sqrt(n)

  print *, "unknown_concentration_mM=", unknown
  print *, "first_order_concentration_mM=", concentration
  print *, "half_life_s=", half_life
  print *, "standard_error=", se

end program python_chemistry_kernel
