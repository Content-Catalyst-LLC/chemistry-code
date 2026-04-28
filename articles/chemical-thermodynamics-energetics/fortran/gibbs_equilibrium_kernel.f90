program gibbs_equilibrium_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8) :: delta_h_kj_mol
  real(8) :: delta_s_j_mol_k
  real(8) :: temperature_k
  real(8) :: delta_g_kj_mol
  real(8) :: equilibrium_constant

  delta_h_kj_mol = -80.0d0
  delta_s_j_mol_k = -100.0d0
  temperature_k = 298.15d0

  delta_g_kj_mol = delta_h_kj_mol - temperature_k * delta_s_j_mol_k / 1000.0d0
  equilibrium_constant = exp(-(delta_g_kj_mol * 1000.0d0) / (R * temperature_k))

  print *, "delta_g_kj_mol=", delta_g_kj_mol
  print *, "equilibrium_constant=", equilibrium_constant

end program gibbs_equilibrium_kernel
