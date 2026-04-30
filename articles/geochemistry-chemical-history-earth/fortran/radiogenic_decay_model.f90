! Geochemistry and the Chemical History of Earth
! Fortran radioactive decay and parent-daughter isotope evolution.
! Synthetic educational code only.
!
! This is not research-grade geochronology or radiological safety modeling.

program radiogenic_decay_model
  implicit none

  integer :: unit_number, step
  real :: half_life_ma, lambda, time_ma, parent_fraction, daughter_fraction

  half_life_ma = 4468.0
  lambda = log(2.0) / half_life_ma

  open(newunit=unit_number, file="../outputs/tables/fortran_radiogenic_decay_model.csv", status="replace", action="write")
  write(unit_number, '(A)') "time_ma,parent_fraction,daughter_fraction"

  do step = 0, 20
    time_ma = real(step) * 250.0
    parent_fraction = exp(-lambda * time_ma)
    daughter_fraction = 1.0 - parent_fraction
    write(unit_number, '(F12.6,A,F12.6,A,F12.6)') time_ma, ",", parent_fraction, ",", daughter_fraction
  end do

  close(unit_number)
  print *, "Fortran radiogenic decay model complete."

end program radiogenic_decay_model
