program first_order_kernel
  implicit none

  real(8) :: c0, k, t, concentration, half_life

  c0 = 1.0d0
  k = 0.15d0
  t = 20.0d0

  concentration = c0 * exp(-k * t)
  half_life = log(2.0d0) / k

  print *, "first_order_concentration_t20=", concentration
  print *, "first_order_half_life=", half_life

end program first_order_kernel
