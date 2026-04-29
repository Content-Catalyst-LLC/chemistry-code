program industrial_process_metric_kernel
  implicit none

  real(8) :: theoretical_product, actual_product, waste, solvent, energy
  real(8) :: reactor_volume, time_h
  real(8) :: yield_fraction, e_factor, solvent_intensity
  real(8) :: energy_intensity, space_time_yield, residence_time

  theoretical_product = 1000.0d0
  actual_product = 910.0d0
  waste = 210.0d0
  solvent = 350.0d0
  energy = 1600.0d0
  reactor_volume = 8.0d0
  time_h = 4.0d0

  yield_fraction = actual_product / theoretical_product
  e_factor = waste / actual_product
  solvent_intensity = solvent / actual_product
  energy_intensity = energy / actual_product
  space_time_yield = actual_product / (reactor_volume * time_h)
  residence_time = reactor_volume / 2.0d0

  print *, "Industrial process metric kernel"
  print *, "Yield fraction:", yield_fraction
  print *, "E-factor:", e_factor
  print *, "Solvent intensity:", solvent_intensity
  print *, "Energy intensity kWh/kg:", energy_intensity
  print *, "Space-time yield kg/m3/h:", space_time_yield
  print *, "Residence time proxy h:", residence_time
  print *, "Responsible-use note: synthetic educational calculation only."
end program industrial_process_metric_kernel
