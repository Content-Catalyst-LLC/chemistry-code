program polymer_metric_kernel
  implicit none

  real(8) :: counts(5), masses(5)
  real(8) :: sum_counts, sum_nm, sum_nm2, Mn, Mw, dispersity
  integer :: i

  counts = (/1000.0d0, 1800.0d0, 2400.0d0, 1600.0d0, 700.0d0/)
  masses = (/25000.0d0, 55000.0d0, 90000.0d0, 135000.0d0, 210000.0d0/)

  sum_counts = 0.0d0
  sum_nm = 0.0d0
  sum_nm2 = 0.0d0

  do i = 1, 5
    sum_counts = sum_counts + counts(i)
    sum_nm = sum_nm + counts(i) * masses(i)
    sum_nm2 = sum_nm2 + counts(i) * masses(i) * masses(i)
  end do

  Mn = sum_nm / sum_counts
  Mw = sum_nm2 / sum_nm
  dispersity = Mw / Mn

  print *, "Polymer molar-mass kernel"
  print *, "Mn g/mol:", Mn
  print *, "Mw g/mol:", Mw
  print *, "Dispersity:", dispersity
  print *, "Responsible-use note: synthetic educational calculation only."
end program polymer_metric_kernel
