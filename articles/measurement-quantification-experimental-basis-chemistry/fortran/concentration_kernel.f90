program concentration_kernel
  implicit none

  real :: mass_g
  real :: molar_mass_g_mol
  real :: volume_l
  real :: moles
  real :: concentration_mol_l

  mass_g = 5.844
  molar_mass_g_mol = 58.44
  volume_l = 0.500

  moles = mass_g / molar_mass_g_mol
  concentration_mol_l = moles / volume_l

  print *, "moles=", moles
  print *, "concentration_mol_l=", concentration_mol_l

end program concentration_kernel
