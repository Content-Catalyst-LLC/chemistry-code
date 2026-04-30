! Environmental Chemistry and the Chemical Conditions of Habitability
! Fortran first-order decay and retardation model.
! Synthetic educational code only.
!
! This is not a regulatory, remediation, legal, or public-health tool.

program environmental_decay_retardation
  implicit none

  real :: kd, r, c365, k
  integer :: unit_number

  kd = kd_l_kg(90.0, 0.001)
  r = retardation_factor(kd, 1.70, 0.30)
  k = decay_constant(365.0)
  c365 = concentration_after_time(8.5, 365.0, 365.0)

  open(newunit=unit_number, file="../outputs/tables/fortran_environmental_decay_retardation.csv", status="replace", action="write")
  write(unit_number, '(A)') "metric,value"
  write(unit_number, '(A,F14.8)') "Kd_L_kg,", kd
  write(unit_number, '(A,F14.8)') "retardation_factor,", r
  write(unit_number, '(A,F14.8)') "decay_constant_per_day,", k
  write(unit_number, '(A,F14.8)') "concentration_day_365,", c365
  close(unit_number)

  print *, "Fortran environmental decay and retardation model complete."

contains

  real function kd_l_kg(koc_l_kg, foc)
    real, intent(in) :: koc_l_kg, foc
    kd_l_kg = koc_l_kg * foc
  end function kd_l_kg

  real function retardation_factor(kd, bulk_density, porosity)
    real, intent(in) :: kd, bulk_density, porosity
    real :: n
    n = max(porosity, 0.01)
    retardation_factor = 1.0 + (bulk_density * kd) / n
  end function retardation_factor

  real function decay_constant(half_life_days)
    real, intent(in) :: half_life_days
    if (half_life_days <= 0.0) then
      decay_constant = 0.0
    else
      decay_constant = log(2.0) / half_life_days
    end if
  end function decay_constant

  real function concentration_after_time(c0, half_life_days, days)
    real, intent(in) :: c0, half_life_days, days
    concentration_after_time = c0 * exp(-decay_constant(half_life_days) * days)
  end function concentration_after_time

end program environmental_decay_retardation
