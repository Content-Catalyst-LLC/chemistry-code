program physical_chemistry_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8), parameter :: F = 96485.33212d0
  real(8) :: K_demo, k_demo, E_demo

  K_demo = exp(-(-20.0d0 * 1000.0d0) / (R * 298.15d0))
  k_demo = 1.0d12 * exp(-(75.0d0 * 1000.0d0) / (R * 298.15d0))
  E_demo = 1.10d0 - (R * 298.15d0 / (2.0d0 * F)) * log(100.0d0)

  print *, "K_demo=", K_demo
  print *, "k_demo=", k_demo
  print *, "E_demo=", E_demo

end program physical_chemistry_kernel
