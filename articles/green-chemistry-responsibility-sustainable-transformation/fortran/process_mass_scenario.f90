! Green Chemistry, Responsibility, and Sustainable Transformation
! Fortran process mass and waste-reduction scenario.
! Synthetic educational code only.

program process_mass_scenario
  implicit none

  integer :: unit_number, step
  real :: product_mass, starting_waste, waste_reduction, waste_mass, e_factor_value, pmi_value, input_mass

  product_mass = 2.4
  starting_waste = 18.0

  open(newunit=unit_number, file="../outputs/tables/fortran_process_mass_scenario.csv", status="replace", action="write")
  write(unit_number, '(A)') "step,waste_reduction_fraction,waste_mass_kg,e_factor,pmi"

  do step = 0, 10
    waste_reduction = real(step) / 10.0
    waste_mass = starting_waste * (1.0 - waste_reduction)
    input_mass = product_mass + waste_mass
    e_factor_value = e_factor(waste_mass, product_mass)
    pmi_value = pmi(input_mass, product_mass)
    write(unit_number, '(I0,A,F10.4,A,F12.6,A,F12.6,A,F12.6)') step, ",", waste_reduction, ",", waste_mass, ",", e_factor_value, ",", pmi_value
  end do

  close(unit_number)
  print *, "Fortran process mass scenario complete."

contains

  real function e_factor(waste_mass, product_mass)
    real, intent(in) :: waste_mass, product_mass
    if (product_mass <= 0.0) then
      e_factor = 0.0
    else
      e_factor = waste_mass / product_mass
    end if
  end function e_factor

  real function pmi(total_input_mass, product_mass)
    real, intent(in) :: total_input_mass, product_mass
    if (product_mass <= 0.0) then
      pmi = 0.0
    else
      pmi = total_input_mass / product_mass
    end if
  end function pmi

end program process_mass_scenario
