program redox_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8), parameter :: F = 96485.33212d0
  real(8) :: ecell, dg, e_nonstandard

  ecell = 0.34d0 - (-0.76d0)
  dg = -2.0d0 * F * ecell / 1000.0d0
  e_nonstandard = 1.10d0 - (R * 298.15d0 / (2.0d0 * F)) * log(100.0d0)

  print *, "E_cell_standard_V=", ecell
  print *, "delta_g_standard_kj_mol=", dg
  print *, "E_nonstandard_V=", e_nonstandard

end program redox_kernel
