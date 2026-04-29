program electrochemical_metric_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8), parameter :: T = 298.15d0
  real(8), parameter :: F = 96485.33212d0
  real(8) :: n, nernst_slope_v, blank_sd, sensitivity, lod

  n = 1.0d0
  nernst_slope_v = R * T / (n * F) * log(10.0d0)

  blank_sd = 0.002081666d0
  sensitivity = 0.0336d0
  lod = 3.0d0 * blank_sd / sensitivity

  print *, "Electrochemical metric kernel"
  print *, "Nernst slope V per decade at 298.15 K:", nernst_slope_v
  print *, "Estimated LOD uM:", lod
  print *, "Responsible-use note: synthetic educational calculation only."
end program electrochemical_metric_kernel
