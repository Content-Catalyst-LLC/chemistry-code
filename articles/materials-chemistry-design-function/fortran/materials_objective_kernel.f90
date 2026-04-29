program materials_objective_kernel
  implicit none

  real(8) :: density, modulus, thermal, recycle, cost
  real(8) :: score

  density = 1.28d0
  modulus = 4.2d0
  thermal = 180.0d0
  recycle = 0.72d0
  cost = 0.35d0

  score = 1.2d0 * ((density - 1.5d0) / 1.0d0)**2 + &
          0.8d0 * ((modulus - 10.0d0) / 25.0d0)**2 + &
          1.0d0 * ((thermal - 300.0d0) / 250.0d0)**2 + &
          1.4d0 * ((recycle - 0.85d0) / 0.25d0)**2 + &
          1.2d0 * ((cost - 0.30d0) / 0.30d0)**2

  print *, "Materials objective-function kernel"
  print *, "Synthetic objective score:", score
  print *, "Responsible-use note: synthetic educational calculation only."
end program materials_objective_kernel
