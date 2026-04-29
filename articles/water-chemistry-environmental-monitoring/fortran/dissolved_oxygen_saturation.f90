program dissolved_oxygen_saturation
  implicit none

  real(8) :: temp_c, do_sat
  integer :: i
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_do_saturation.csv"

  ! Simplified freshwater dissolved oxygen saturation approximation at 1 atm.
  ! Educational only; does not include salinity or pressure corrections.
  ! DOsat mg/L approximately:
  ! 14.652 - 0.41022*T + 0.007991*T^2 - 0.000077774*T^3

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "temperature_c,do_saturation_mg_L"

  do i = 0, 30, 5
     temp_c = dble(i)
     do_sat = 14.652d0 - 0.41022d0 * temp_c + 0.007991d0 * temp_c**2 - 0.000077774d0 * temp_c**3
     write(10, '(F8.2,A,F10.4)') temp_c, ",", do_sat
  end do

  close(10)

  print *, "Dissolved oxygen saturation approximation complete."
end program dissolved_oxygen_saturation
