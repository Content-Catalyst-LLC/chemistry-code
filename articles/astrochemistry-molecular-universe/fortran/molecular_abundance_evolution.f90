! Astrochemistry and the Molecular Universe
! Fortran molecular abundance evolution model.
! Synthetic educational code only.
!
! This is not a research-grade chemical network solver.

program molecular_abundance_evolution
  implicit none

  integer :: unit_number, step
  real :: time_yr, abundance, formation_rate, destruction_rate, dt, production, loss

  abundance = 1.0e-10
  formation_rate = 2.0e-12
  destruction_rate = 1.5e-6
  dt = 1000.0

  open(newunit=unit_number, file="../outputs/tables/fortran_molecular_abundance_evolution.csv", status="replace", action="write")
  write(unit_number, '(A)') "time_yr,abundance_fraction,production,loss"

  do step = 0, 200
    time_yr = real(step) * dt
    production = formation_rate * dt
    loss = destruction_rate * abundance * dt
    abundance = max(abundance + production - loss, 0.0)

    if (mod(step, 10) == 0) then
      write(unit_number, '(F12.2,A,ES14.6,A,ES14.6,A,ES14.6)') time_yr, ",", abundance, ",", production, ",", loss
    end if
  end do

  close(unit_number)
  print *, "Fortran molecular abundance evolution complete."

end program molecular_abundance_evolution
