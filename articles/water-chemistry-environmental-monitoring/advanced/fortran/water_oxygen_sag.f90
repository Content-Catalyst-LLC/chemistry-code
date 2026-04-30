! Water Chemistry and Environmental Monitoring
! Fortran dissolved-oxygen sag and recovery model.
! Synthetic educational code only.
!
! This is not a regulatory, public-health, permit, or operational water-quality model.

program water_oxygen_sag
  implicit none

  integer :: unit_number, hour
  real :: saturation, initial_do, max_deficit, recovery_rate, deficit, modeled_do

  saturation = 8.5
  initial_do = 4.6
  max_deficit = saturation - initial_do
  recovery_rate = 0.045

  open(newunit=unit_number, file="../outputs/tables/fortran_water_oxygen_sag.csv", status="replace", action="write")
  write(unit_number, '(A)') "hour,modeled_dissolved_oxygen_mg_L,modeled_oxygen_deficit_mg_L,oxygen_stress_index"

  do hour = 0, 120, 6
    deficit = max_deficit * exp(-recovery_rate * real(hour))
    modeled_do = max(saturation - deficit, 0.0)

    write(unit_number, '(I0,A,F12.6,A,F12.6,A,F12.6)') hour, ",", modeled_do, ",", deficit, ",", oxygen_stress(modeled_do, saturation)
  end do

  close(unit_number)
  print *, "Fortran water oxygen sag model complete."

contains

  real function clamp01(x)
    real, intent(in) :: x
    clamp01 = max(0.0, min(1.0, x))
  end function clamp01

  real function oxygen_stress(dissolved_oxygen, saturation_value)
    real, intent(in) :: dissolved_oxygen, saturation_value
    real :: low_do, deficit_component, deficit

    deficit = max(saturation_value - dissolved_oxygen, 0.0)
    low_do = clamp01((6.0 - dissolved_oxygen) / 6.0)
    deficit_component = clamp01(deficit / 6.0)
    oxygen_stress = clamp01(0.60 * low_do + 0.40 * deficit_component)
  end function oxygen_stress

end program water_oxygen_sag
