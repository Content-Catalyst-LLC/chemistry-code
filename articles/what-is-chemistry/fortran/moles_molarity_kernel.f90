program moles_molarity_kernel
  implicit none

  real :: mass_g
  real :: molar_mass_g_mol
  real :: volume_l
  real :: moles
  real :: molarity

  mass_g = 5.844
  molar_mass_g_mol = 58.44
  volume_l = 0.500

  moles = mass_g / molar_mass_g_mol
  molarity = moles / volume_l

  print *, "moles=", moles
  print *, "molarity_mol_l=", molarity

end program moles_molarity_kernel
