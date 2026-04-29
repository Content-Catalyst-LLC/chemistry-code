program computational_chemistry_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8), parameter :: kB = 1.380649d-23
  real(8), parameter :: h = 6.62607015d-34
  real(8) :: boltzmann, lj, tanimoto, rate
  real(8) :: ratio

  boltzmann = exp(-(2.5d0 * 1000.0d0) / (R * 298.15d0))
  ratio = 1.0d0 / 1.12d0
  lj = 4.0d0 * 1.0d0 * (ratio ** 12 - ratio ** 6)
  tanimoto = 3.0d0 / (5.0d0 + 4.0d0 - 3.0d0)
  rate = (kB * 298.15d0 / h) * exp(-(55.0d0 * 1000.0d0) / (R * 298.15d0))

  print *, "boltzmann_weight=", boltzmann
  print *, "lennard_jones=", lj
  print *, "tanimoto=", tanimoto
  print *, "tst_rate=", rate

end program computational_chemistry_kernel
