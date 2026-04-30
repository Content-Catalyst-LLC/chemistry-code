! Toxicology, Exposure, and Chemical Risk
! Fortran exposure dose and margin-of-exposure model.
! Synthetic educational code only.
!
! This is not a public-health, clinical, legal, or regulatory tool.

program exposure_moe_model
  implicit none

  real :: cdi, dose, hq, moe
  integer :: unit_number

  cdi = chronic_daily_intake(0.010, 2.0, 350.0, 30.0, 70.0, 10950.0)
  dose = absorbed_dose(cdi, 0.95)
  hq = hazard_quotient(dose, 0.0003)
  moe = margin_of_exposure(0.008, dose)

  open(newunit=unit_number, file="../outputs/tables/fortran_exposure_moe_model.csv", status="replace", action="write")
  write(unit_number, '(A)') "metric,value"
  write(unit_number, '(A,F14.8)') "chronic_daily_intake,", cdi
  write(unit_number, '(A,F14.8)') "absorbed_dose,", dose
  write(unit_number, '(A,F14.8)') "hazard_quotient,", hq
  write(unit_number, '(A,F14.8)') "margin_of_exposure,", moe
  close(unit_number)

  print *, "Fortran exposure MOE model complete."

contains

  real function chronic_daily_intake(concentration, intake_rate, exposure_frequency, exposure_duration, body_weight, averaging_time)
    real, intent(in) :: concentration, intake_rate, exposure_frequency, exposure_duration, body_weight, averaging_time

    if (body_weight <= 0.0 .or. averaging_time <= 0.0) then
      chronic_daily_intake = 0.0
    else
      chronic_daily_intake = concentration * intake_rate * exposure_frequency * exposure_duration / (body_weight * averaging_time)
    end if
  end function chronic_daily_intake

  real function absorbed_dose(cdi, absorption_fraction)
    real, intent(in) :: cdi, absorption_fraction
    absorbed_dose = cdi * absorption_fraction
  end function absorbed_dose

  real function hazard_quotient(dose, reference_dose)
    real, intent(in) :: dose, reference_dose

    if (reference_dose <= 0.0) then
      hazard_quotient = 0.0
    else
      hazard_quotient = dose / reference_dose
    end if
  end function hazard_quotient

  real function margin_of_exposure(point_of_departure, dose)
    real, intent(in) :: point_of_departure, dose

    if (dose <= 0.0) then
      margin_of_exposure = 0.0
    else
      margin_of_exposure = point_of_departure / dose
    end if
  end function margin_of_exposure

end program exposure_moe_model
