program kinetics_kernel
  implicit none

  real :: initial_concentration
  real :: rate_constant
  real :: time
  real :: concentration

  initial_concentration = 1.0
  rate_constant = 0.15
  time = 10.0

  concentration = initial_concentration * exp(-rate_constant * time)

  print *, "first_order_concentration_t10=", concentration

end program kinetics_kernel
