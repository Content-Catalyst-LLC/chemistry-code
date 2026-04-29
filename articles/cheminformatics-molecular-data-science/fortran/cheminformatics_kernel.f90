program cheminformatics_kernel
  implicit none

  real(8) :: tanimoto, pic50, distance
  real(8) :: ic50_nm, ic50_m

  tanimoto = 3.0d0 / (5.0d0 + 4.0d0 - 3.0d0)

  ic50_nm = 50.0d0
  ic50_m = ic50_nm * 1.0d-9
  pic50 = -log10(ic50_m)

  distance = sqrt((1.0d0 - 1.5d0)**2 + (2.0d0 - 2.5d0)**2 + (3.0d0 - 4.0d0)**2)

  print *, "tanimoto=", tanimoto
  print *, "pIC50=", pic50
  print *, "distance=", distance

end program cheminformatics_kernel
