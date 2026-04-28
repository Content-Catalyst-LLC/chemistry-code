program lennard_jones_kernel
  implicit none

  real(8) :: epsilon_kj_mol
  real(8) :: sigma_angstrom
  real(8) :: r_angstrom
  real(8) :: ratio
  real(8) :: u_kj_mol

  epsilon_kj_mol = 0.997d0
  sigma_angstrom = 3.40d0
  r_angstrom = 2.0d0 ** (1.0d0 / 6.0d0) * sigma_angstrom

  ratio = sigma_angstrom / r_angstrom
  u_kj_mol = 4.0d0 * epsilon_kj_mol * (ratio**12 - ratio**6)

  print *, "r_min_angstrom=", r_angstrom
  print *, "u_min_kj_mol=", u_kj_mol

end program lennard_jones_kernel
