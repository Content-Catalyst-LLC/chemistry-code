program uncertainty_kernel
  implicit none

  real :: components(6)
  real :: sumsq
  real :: uc
  real :: expanded
  integer :: i

  components = (/0.004, 0.006, 0.010, 0.015, 0.012, 0.020/)
  sumsq = 0.0

  do i = 1, 6
    sumsq = sumsq + components(i) * components(i)
  end do

  uc = sqrt(sumsq)
  expanded = 2.0 * uc

  print *, "combined_standard_uncertainty=", uc
  print *, "expanded_uncertainty=", expanded

end program uncertainty_kernel
