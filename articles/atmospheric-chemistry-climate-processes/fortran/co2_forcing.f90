program co2_forcing
  implicit none

  real(8) :: current_ppm, reference_ppm, forcing
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_co2_forcing.csv"

  current_ppm = 423.0d0
  reference_ppm = 280.0d0
  forcing = 5.35d0 * log(current_ppm / reference_ppm)

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "current_ppm,reference_ppm,forcing_W_m2"
  write(10, '(F10.3,A,F10.3,A,F10.5)') current_ppm, ",", reference_ppm, ",", forcing
  close(10)

  print *, "Approximate CO2 forcing relative to reference concentration:"
  print *, forcing, "W/m2"
end program co2_forcing
