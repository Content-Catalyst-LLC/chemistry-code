! Ocean Chemistry and the Carbonate System
! Fortran CO2 uptake and pH-shift scenario model.
! Synthetic educational code only.
!
! This is not a research-grade carbonate-system solver or policy model.

program ocean_co2_pH_scenario
  implicit none

  integer :: unit_number, step
  real :: initial_pH, pco2, carbonate, omega, co2_increment

  initial_pH = 8.10
  pco2 = 400.0
  carbonate = 190.0
  co2_increment = 25.0

  open(newunit=unit_number, file="../outputs/tables/fortran_ocean_co2_pH_scenario.csv", status="replace", action="write")
  write(unit_number, '(A)') "step,pco2_uatm,modeled_pH,carbonate_umol_kg,omega_aragonite,acidification_pressure"

  do step = 0, 20
    omega = saturation_proxy(carbonate, 10.3, 60.0)
    write(unit_number, '(I0,A,F12.6,A,F12.6,A,F12.6,A,F12.6,A,F12.6)') &
      step, ",", pco2, ",", initial_pH, ",", carbonate, ",", omega, ",", acidification_pressure(initial_pH, pco2, carbonate, omega)

    pco2 = pco2 + co2_increment
    initial_pH = initial_pH - 0.008
    carbonate = max(carbonate - 3.5, 10.0)
  end do

  close(unit_number)
  print *, "Fortran ocean CO2 pH scenario complete."

contains

  real function clamp01(x)
    real, intent(in) :: x
    clamp01 = max(0.0, min(1.0, x))
  end function clamp01

  real function saturation_proxy(carbonate_umol_kg, calcium_mmol_kg, ksp_proxy)
    real, intent(in) :: carbonate_umol_kg, calcium_mmol_kg, ksp_proxy
    real :: calcium_umol_kg

    calcium_umol_kg = calcium_mmol_kg * 1000.0
    if (ksp_proxy <= 0.0) then
      saturation_proxy = 0.0
    else
      saturation_proxy = (carbonate_umol_kg * calcium_umol_kg) / (ksp_proxy * 100000.0)
    end if
  end function saturation_proxy

  real function acidification_pressure(pH, pco2, carbonate_umol_kg, omega_aragonite)
    real, intent(in) :: pH, pco2, carbonate_umol_kg, omega_aragonite
    real :: ph_component, co2_component, carbonate_component, saturation_component

    ph_component = clamp01((8.2 - pH) / 0.7)
    co2_component = clamp01((pco2 - 400.0) / 800.0)
    carbonate_component = clamp01((180.0 - carbonate_umol_kg) / 180.0)
    saturation_component = clamp01((3.0 - omega_aragonite) / 3.0)

    acidification_pressure = clamp01(0.30 * ph_component + 0.25 * co2_component + 0.25 * carbonate_component + 0.20 * saturation_component)
  end function acidification_pressure

end program ocean_co2_pH_scenario
