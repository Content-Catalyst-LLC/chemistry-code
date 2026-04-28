program distance_kernel
  implicit none

  real(8) :: ox, oy, oz
  real(8) :: hx, hy, hz
  real(8) :: distance

  ox = 0.0d0
  oy = 0.0d0
  oz = 0.0d0

  hx = 0.958d0
  hy = 0.0d0
  hz = 0.0d0

  distance = sqrt((ox - hx)**2 + (oy - hy)**2 + (oz - hz)**2)

  print *, "OH distance angstrom=", distance

end program distance_kernel
