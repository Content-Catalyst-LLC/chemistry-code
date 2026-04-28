program isotope_mass_kernel
  implicit none

  real(8) :: cl35_mass, cl37_mass
  real(8) :: cl35_abundance, cl37_abundance
  real(8) :: weighted_mass

  cl35_mass = 34.96885268d0
  cl37_mass = 36.96590260d0
  cl35_abundance = 0.7576d0
  cl37_abundance = 0.2424d0

  weighted_mass = cl35_mass * cl35_abundance + cl37_mass * cl37_abundance

  print *, "chlorine_weighted_atomic_mass_u=", weighted_mass

end program isotope_mass_kernel
