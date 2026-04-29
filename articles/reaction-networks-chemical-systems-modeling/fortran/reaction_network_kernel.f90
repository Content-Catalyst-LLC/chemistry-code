program reaction_network_kernel
  implicit none

  real(8) :: A, B, C, D, E
  real(8) :: k1, k2, k3, k4, dt, t, total_time
  real(8) :: r1, r2, r3, r4

  A = 1.0d0
  B = 0.0d0
  C = 0.0d0
  D = 0.0d0
  E = 0.0d0

  k1 = 0.20d0
  k2 = 0.08d0
  k3 = 0.05d0
  k4 = 0.03d0
  dt = 0.25d0
  total_time = 50.0d0

  t = 0.0d0
  do while (t <= total_time)
    r1 = k1 * A
    r2 = k2 * B
    r3 = k3 * A
    r4 = k4 * B

    A = max(A + (-r1 - r3) * dt, 0.0d0)
    B = max(B + (r1 - r2 - r4) * dt, 0.0d0)
    C = max(C + r2 * dt, 0.0d0)
    D = max(D + r3 * dt, 0.0d0)
    E = max(E + r4 * dt, 0.0d0)

    t = t + dt
  end do

  print *, "A_final=", A
  print *, "B_final=", B
  print *, "C_final=", C
  print *, "D_final=", D
  print *, "E_final=", E

end program reaction_network_kernel
