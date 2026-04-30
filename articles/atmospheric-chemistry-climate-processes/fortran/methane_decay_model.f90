! Atmospheric Chemistry and Climate Processes
! Fortran methane perturbation decay model.
! Synthetic educational code only.
!
! This is not a climate attribution, regulatory, emissions, or forecasting model.

program methane_decay_model
  implicit none

  integer :: unit_number, year
  real :: initial_ppb, lifetime_days, days, concentration, fraction_remaining

  initial_ppb = 1950.0
  lifetime_days = 4380.0

  open(newunit=unit_number, file="../outputs/tables/fortran_methane_decay_model.csv", status="replace", action="write")
  write(unit_number, '(A)') "year,modeled_ch4_ppb,fraction_remaining"

  do year = 0, 60, 2
    days = real(year) * 365.25
    concentration = initial_ppb * exp(-days / lifetime_days)
    fraction_remaining = concentration / initial_ppb
    write(unit_number, '(I0,A,F12.6,A,F12.6)') year, ",", concentration, ",", fraction_remaining
  end do

  close(unit_number)
  print *, "Fortran methane decay model complete."

end program methane_decay_model
