program r_chemistry_kernel
  implicit none

  real(8), dimension(3) :: x
  real(8) :: mean_x, sd_x, se_x, rsd, unknown
  integer :: n

  x = (/1.02d0, 1.05d0, 0.99d0/)
  n = 3

  mean_x = sum(x) / n
  sd_x = sqrt(sum((x - mean_x) ** 2) / (n - 1))
  se_x = sd_x / sqrt(real(n, 8))
  rsd = 100.0d0 * sd_x / mean_x
  unknown = (0.95d0 - 0.02d0) / 0.30d0

  print *, "mean=", mean_x
  print *, "sample_sd=", sd_x
  print *, "standard_error=", se_x
  print *, "rsd_percent=", rsd
  print *, "unknown_concentration=", unknown

end program r_chemistry_kernel
