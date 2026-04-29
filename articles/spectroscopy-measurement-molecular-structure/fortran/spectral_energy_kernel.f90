program spectral_energy_kernel
  implicit none

  real(8), parameter :: h = 6.62607015d-34
  real(8), parameter :: c = 2.99792458d8
  real(8), parameter :: avogadro = 6.02214076d23
  real(8) :: wavenumber_cm, energy_kj_mol

  wavenumber_cm = 1718.0d0
  energy_kj_mol = h * c * wavenumber_cm * 100.0d0 * avogadro / 1000.0d0

  print *, "Spectral energy kernel"
  print *, "Wavenumber cm^-1:", wavenumber_cm
  print *, "Photon energy kJ/mol:", energy_kj_mol
  print *, "Responsible-use note: synthetic educational conversion only."
end program spectral_energy_kernel
