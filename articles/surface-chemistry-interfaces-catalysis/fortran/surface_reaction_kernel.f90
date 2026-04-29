program surface_reaction_kernel
  implicit none

  real(8) :: KA, KB, PA, PB, denominator, thetaA, thetaB
  real(8) :: Ea, R, T, Apre, k, site_density, rate_proxy

  KA = 1.8d0
  KB = 0.7d0
  PA = 1.0d0
  PB = 0.5d0
  Ea = 58.0d0
  R = 0.008314d0
  T = 550.0d0
  Apre = 1.0d5
  site_density = 120.0d0

  denominator = 1.0d0 + KA * PA + KB * PB
  thetaA = KA * PA / denominator
  thetaB = KB * PB / denominator
  k = Apre * exp(-Ea / (R * T))
  rate_proxy = k * thetaA * thetaB * site_density

  print *, "Surface reaction kernel"
  print *, "theta A:", thetaA
  print *, "theta B:", thetaB
  print *, "rate proxy:", rate_proxy
  print *, "Responsible-use note: synthetic educational calculation only."
end program surface_reaction_kernel
