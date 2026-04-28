program hydrogen_levels_kernel
  implicit none

  integer :: n
  real(8) :: energy_ev

  do n = 1, 6
    energy_ev = -13.6d0 / dble(n * n)
    print *, "n=", n, " energy_eV=", energy_ev
  end do

end program hydrogen_levels_kernel
