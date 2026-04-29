program catalysis_kernel
  implicit none

  real(8), parameter :: R = 8.314462618d0
  real(8) :: rate_enhancement, ton, tof, theta

  rate_enhancement = exp((25.0d0 * 1000.0d0) / (R * 298.15d0))
  ton = 0.05d0 / 0.0005d0
  tof = ton / 3600.0d0
  theta = (1.5d0 * 1.0d0) / (1.0d0 + 1.5d0 * 1.0d0)

  print *, "rate_enhancement=", rate_enhancement
  print *, "TON=", ton
  print *, "TOF=", tof
  print *, "theta=", theta

end program catalysis_kernel
