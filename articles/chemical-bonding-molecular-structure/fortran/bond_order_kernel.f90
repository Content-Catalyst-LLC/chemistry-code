program bond_order_kernel
  implicit none

  real(8) :: bonding_electrons
  real(8) :: antibonding_electrons
  real(8) :: bond_order

  bonding_electrons = 2.0d0
  antibonding_electrons = 0.0d0

  bond_order = (bonding_electrons - antibonding_electrons) / 2.0d0

  print *, "h2_bond_order=", bond_order

end program bond_order_kernel
