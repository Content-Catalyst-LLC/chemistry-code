program nanoscale_metric_kernel
  implicit none

  real(8) :: core_diameter_nm, hydrodynamic_diameter_nm
  real(8) :: surface_area_to_volume
  real(8) :: kB, T, eta, diffusion

  core_diameter_nm = 18.0d0
  hydrodynamic_diameter_nm = 24.0d0

  surface_area_to_volume = 6.0d0 / core_diameter_nm

  kB = 1.380649d-23
  T = 298.15d0
  eta = 0.00089d0

  diffusion = kB * T / (3.0d0 * 3.141592653589793d0 * eta * hydrodynamic_diameter_nm * 1.0d-9)

  print *, "Nanoscale metric kernel"
  print *, "Surface-area-to-volume nm^-1:", surface_area_to_volume
  print *, "Diffusion estimate m^2/s:", diffusion
  print *, "Responsible-use note: synthetic educational calculation only."
end program nanoscale_metric_kernel
