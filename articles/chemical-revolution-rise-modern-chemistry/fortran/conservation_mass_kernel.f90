program conservation_mass_kernel
  implicit none

  real :: reactant_mass_g
  real :: product_mass_g
  real :: difference_g

  reactant_mass_g = 44.0
  product_mass_g = 44.0

  difference_g = product_mass_g - reactant_mass_g

  print *, "mass_difference_g=", difference_g

end program conservation_mass_kernel
