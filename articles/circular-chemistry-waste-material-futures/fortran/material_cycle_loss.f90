! Circular Chemistry, Waste, and Material Futures
! Fortran repeated-cycle material loss scenario.
! Synthetic educational code only.

program material_cycle_loss
  implicit none

  integer :: unit_number, cycle
  real :: initial_mass, loss_fraction, remaining_mass, recovered_mass

  initial_mass = 1000.0
  loss_fraction = 0.12
  remaining_mass = initial_mass

  open(newunit=unit_number, file="../outputs/tables/fortran_material_cycle_loss.csv", status="replace", action="write")
  write(unit_number, '(A)') "cycle,remaining_mass_kg,recovered_this_cycle_kg,lost_this_cycle_kg"

  do cycle = 0, 10
    recovered_mass = remaining_mass * (1.0 - loss_fraction)
    write(unit_number, '(I0,A,F12.6,A,F12.6,A,F12.6)') cycle, ",", remaining_mass, ",", recovered_mass, ",", remaining_mass - recovered_mass
    remaining_mass = recovered_mass
  end do

  close(unit_number)
  print *, "Fortran material cycle loss model complete."

end program material_cycle_loss
