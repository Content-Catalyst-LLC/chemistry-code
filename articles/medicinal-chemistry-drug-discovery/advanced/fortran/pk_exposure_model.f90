! Medicinal Chemistry and Drug Discovery
! Fortran PK exposure intuition model.
! Synthetic educational code only.
!
! This is not a dosing model, clinical model, or regulatory PK model.

program pk_exposure_model
  implicit none

  real :: half_life_hr, auc_proxy, cmax_proxy
  integer :: unit_number

  half_life_hr = half_life_from_clearance_vd(18.0, 2.1)
  auc_proxy = auc_from_dose_clearance(10.0, 18.0)
  cmax_proxy = cmax_from_dose_vd(10.0, 2.1)

  open(newunit=unit_number, file="../outputs/tables/fortran_pk_exposure_model.csv", status="replace", action="write")
  write(unit_number, '(A)') "metric,value"
  write(unit_number, '(A,F12.6)') "half_life_hr,", half_life_hr
  write(unit_number, '(A,F12.6)') "auc_proxy,", auc_proxy
  write(unit_number, '(A,F12.6)') "cmax_proxy,", cmax_proxy
  close(unit_number)

  print *, "Fortran PK exposure model complete."

contains

  real function half_life_from_clearance_vd(clearance_ml_min_kg, vd_l_kg)
    real, intent(in) :: clearance_ml_min_kg, vd_l_kg
    real :: clearance_l_hr_kg

    clearance_l_hr_kg = clearance_ml_min_kg * 0.06
    if (clearance_l_hr_kg <= 0.0) then
      half_life_from_clearance_vd = 0.0
    else
      half_life_from_clearance_vd = 0.693 * vd_l_kg / clearance_l_hr_kg
    end if
  end function half_life_from_clearance_vd

  real function auc_from_dose_clearance(dose_mg_kg, clearance_ml_min_kg)
    real, intent(in) :: dose_mg_kg, clearance_ml_min_kg
    real :: clearance_l_hr_kg

    clearance_l_hr_kg = clearance_ml_min_kg * 0.06
    if (clearance_l_hr_kg <= 0.0) then
      auc_from_dose_clearance = 0.0
    else
      auc_from_dose_clearance = dose_mg_kg / clearance_l_hr_kg
    end if
  end function auc_from_dose_clearance

  real function cmax_from_dose_vd(dose_mg_kg, vd_l_kg)
    real, intent(in) :: dose_mg_kg, vd_l_kg

    if (vd_l_kg <= 0.0) then
      cmax_from_dose_vd = 0.0
    else
      cmax_from_dose_vd = dose_mg_kg / vd_l_kg
    end if
  end function cmax_from_dose_vd

end program pk_exposure_model
