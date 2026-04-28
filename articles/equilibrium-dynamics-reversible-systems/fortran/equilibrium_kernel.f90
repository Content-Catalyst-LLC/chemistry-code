program equilibrium_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8) :: K, total, Aeq, Beq, Q, T, delta_g

  K = 4.0d0
  total = 1.0d0
  Aeq = total / (1.0d0 + K)
  Beq = total - Aeq

  Q = 0.5d0
  T = 298.15d0
  delta_g = R * T * log(Q / K) / 1000.0d0

  print *, "A_eq=", Aeq
  print *, "B_eq=", Beq
  print *, "delta_g_kj_mol=", delta_g

end program equilibrium_kernel
