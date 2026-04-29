program mass_error_resolution_kernel
  implicit none

  real(8) :: observed_mz, theoretical_mz, ppm_error
  real(8) :: mass, delta_m, resolution

  observed_mz = 195.0878d0
  theoretical_mz = 195.08765d0

  ppm_error = (observed_mz - theoretical_mz) / theoretical_mz * 1000000.0d0

  mass = 451.213d0
  delta_m = 0.015d0
  resolution = mass / delta_m

  print *, "Mass spectrometry metric kernel"
  print *, "Observed m/z:", observed_mz
  print *, "Theoretical m/z:", theoretical_mz
  print *, "ppm error:", ppm_error
  print *, "Resolution:", resolution
  print *, "Responsible-use note: synthetic educational calculation only."
end program mass_error_resolution_kernel
