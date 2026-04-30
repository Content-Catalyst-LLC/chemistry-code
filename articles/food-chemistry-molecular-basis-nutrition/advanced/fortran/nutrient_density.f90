! Food Chemistry and the Molecular Basis of Nutrition
! Fortran nutrient-density and retention example.
! Synthetic educational code only.

program nutrient_density_model
  implicit none

  real :: lentil_nd, orange_retained_c
  integer :: unit_number

  lentil_nd = nutrient_density(18.0, 15.0, 730.0, 230.0)
  orange_retained_c = retained_vitamin_c(70.0, 0.82)

  open(newunit=unit_number, file="../outputs/tables/fortran_nutrient_density.csv", status="replace", action="write")
  write(unit_number, '(A)') "metric,value"
  write(unit_number, '(A,F10.6)') "lentil_nutrient_density,", lentil_nd
  write(unit_number, '(A,F10.6)') "orange_retained_vitamin_c_mg,", orange_retained_c
  close(unit_number)

  print *, "Fortran nutrient density model complete."

contains

  real function clamp01(x)
    real, intent(in) :: x
    clamp01 = max(0.0, min(1.0, x))
  end function clamp01

  real function nutrient_density(protein_g, fiber_g, potassium_mg, energy_kcal)
    real, intent(in) :: protein_g, fiber_g, potassium_mg, energy_kcal
    real :: beneficial, energy_factor

    beneficial = 0.40 * clamp01(protein_g / 25.0) + &
                 0.35 * clamp01(fiber_g / 12.0) + &
                 0.25 * clamp01(potassium_mg / 800.0)

    energy_factor = max(energy_kcal / 100.0, 0.5)
    nutrient_density = beneficial / energy_factor
  end function nutrient_density

  real function retained_vitamin_c(vitamin_c_mg, retention_factor)
    real, intent(in) :: vitamin_c_mg, retention_factor
    retained_vitamin_c = vitamin_c_mg * retention_factor
  end function retained_vitamin_c

end program nutrient_density_model
