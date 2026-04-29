program battery_metric_kernel
  implicit none

  real(8) :: voltage, specific_capacity, active_mass
  real(8) :: cell_capacity_mAh, cell_energy_Wh
  real(8) :: discharge_capacity, charge_capacity, coulombic_efficiency
  real(8) :: R, T, F, n, Qrxn, E0, E

  voltage = 3.2d0
  specific_capacity = 160.0d0
  active_mass = 12.0d0

  cell_capacity_mAh = specific_capacity * active_mass
  cell_energy_Wh = cell_capacity_mAh * voltage / 1000.0d0

  discharge_capacity = 1843.0d0
  charge_capacity = 1847.0d0
  coulombic_efficiency = discharge_capacity / charge_capacity

  R = 8.314462618d0
  T = 298.15d0
  F = 96485.33212d0
  n = 1.0d0
  Qrxn = 0.1d0
  E0 = 3.4d0
  E = E0 - (R * T / (n * F)) * log(Qrxn)

  print *, "Battery metric kernel"
  print *, "Cell capacity mAh:", cell_capacity_mAh
  print *, "Cell energy Wh:", cell_energy_Wh
  print *, "Coulombic efficiency:", coulombic_efficiency
  print *, "Nernst-style potential V:", E
  print *, "Responsible-use note: synthetic educational calculation only."
end program battery_metric_kernel
