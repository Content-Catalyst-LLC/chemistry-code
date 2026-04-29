program quantum_chemistry_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8), parameter :: kB = 1.380649d-23
  real(8), parameter :: h = 6.62607015d-34
  real(8) :: ea, eb, v, trace, diff, split, e1, e2
  real(8) :: boltzmann, rate

  ea = -10.0d0
  eb = -8.0d0
  v = -2.0d0

  trace = ea + eb
  diff = ea - eb
  split = sqrt(diff ** 2 + 4.0d0 * v ** 2)

  e1 = (trace - split) / 2.0d0
  e2 = (trace + split) / 2.0d0

  boltzmann = exp(-(25.0d0 * 1000.0d0) / (R * 298.15d0))
  rate = (kB * 298.15d0 / h) * exp(-(50.0d0 * 1000.0d0) / (R * 298.15d0))

  print *, "two_level_E1=", e1
  print *, "two_level_E2=", e2
  print *, "boltzmann_weight=", boltzmann
  print *, "tst_rate=", rate

end program quantum_chemistry_kernel
