program weak_acid_kernel
  implicit none

  real(8) :: Ka, C, H, pH, buffer_pH

  Ka = 1.8d-5
  C = 0.100d0

  H = (-Ka + sqrt(Ka**2 + 4.0d0 * Ka * C)) / 2.0d0
  pH = -log10(H)

  buffer_pH = 4.76d0 + log10(0.120d0 / 0.100d0)

  print *, "weak_acid_hydronium=", H
  print *, "weak_acid_pH=", pH
  print *, "buffer_pH=", buffer_pH

end program weak_acid_kernel
