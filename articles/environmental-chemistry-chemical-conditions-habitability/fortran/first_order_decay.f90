program first_order_decay
  implicit none

  integer :: day
  real(8) :: c0, k, concentration, half_life
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_first_order_decay.csv"

  c0 = 100.0d0
  k = 0.08d0
  half_life = log(2.0d0) / k

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "day,concentration_ug_L,fraction_remaining,half_life_days"

  do day = 0, 90, 5
     concentration = c0 * exp(-k * dble(day))
     write(10, '(I0,A,F10.4,A,F10.6,A,F10.4)') day, ",", concentration, ",", concentration / c0, ",", half_life
  end do

  close(10)

  print *, "First-order environmental decay model complete."
  print *, "Half-life days:", half_life
end program first_order_decay
