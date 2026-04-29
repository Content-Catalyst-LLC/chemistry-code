program chromatography_metric_kernel
  implicit none

  real(8) :: tR_A, tR_B, w_A, w_B, tM, resolution, k_A, k_B, alpha

  tM = 0.92d0
  tR_A = 2.85d0
  tR_B = 4.10d0
  w_A = 0.25d0
  w_B = 0.31d0

  k_A = (tR_A - tM) / tM
  k_B = (tR_B - tM) / tM
  alpha = k_B / k_A
  resolution = 2.0d0 * (tR_B - tR_A) / (w_A + w_B)

  print *, "Chromatography metric kernel"
  print *, "Retention factor A:", k_A
  print *, "Retention factor B:", k_B
  print *, "Selectivity alpha:", alpha
  print *, "Resolution Rs:", resolution
  print *, "Responsible-use note: synthetic educational calculation only."
end program chromatography_metric_kernel
