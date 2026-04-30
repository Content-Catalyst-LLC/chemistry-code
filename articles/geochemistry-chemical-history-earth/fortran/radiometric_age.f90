program radiometric_age
  implicit none

  real(8) :: parent, daughter, lambda, age_years, age_ma
  integer :: i
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_radiometric_age.csv"

  real(8), dimension(4) :: daughter_values = (/0.18d0, 0.35d0, 0.28d0, 0.50d0/)

  parent = 1.0d0
  lambda = 1.55125d-10

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "case,parent_units,radiogenic_daughter_units,age_Ma_simplified"

  do i = 1, 4
     daughter = daughter_values(i)
     age_years = (1.0d0 / lambda) * log(1.0d0 + daughter / parent)
     age_ma = age_years / 1.0d6
     write(10, '(I0,A,F8.4,A,F8.4,A,F12.4)') i, ",", parent, ",", daughter, ",", age_ma
  end do

  close(10)

  print *, "Simplified radiometric age calculations complete."
end program radiometric_age
