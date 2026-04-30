! Soil Chemistry, Nutrient Cycles, and Land Systems
! Fortran mineralization and nutrient-pool dynamics.
! Synthetic educational code only.
!
! This is not an agronomic prescription or fertilizer recommendation model.

program soil_nitrogen_mineralization
  implicit none

  integer :: unit_number, day
  real :: organic_n_pool, mineral_n, mineralization_rate, immobilization_fraction, net_release

  organic_n_pool = 1800.0
  mineral_n = 20.0
  mineralization_rate = 0.0025
  immobilization_fraction = 0.35

  open(newunit=unit_number, file="../outputs/tables/fortran_soil_nitrogen_mineralization.csv", status="replace", action="write")
  write(unit_number, '(A)') "day,organic_n_pool,mineral_n,net_release"

  do day = 0, 180, 10
    net_release = organic_n_pool * mineralization_rate * (1.0 - immobilization_fraction)
    mineral_n = mineral_n + net_release
    organic_n_pool = max(organic_n_pool - organic_n_pool * mineralization_rate, 0.0)

    write(unit_number, '(I0,A,F12.6,A,F12.6,A,F12.6)') day, ",", organic_n_pool, ",", mineral_n, ",", net_release
  end do

  close(unit_number)
  print *, "Fortran soil nitrogen mineralization model complete."

end program soil_nitrogen_mineralization
