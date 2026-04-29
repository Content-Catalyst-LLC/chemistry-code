program semiconductor_metric_kernel
  implicit none

  real(8) :: absorption_edge_nm, edge_band_gap_eV
  real(8) :: electron_mobility, hole_mobility, carrier_lifetime_ns
  real(8) :: mobility_balance, transport_proxy
  real(8) :: q, n, p, conductivity_proxy

  absorption_edge_nm = 800.0d0
  edge_band_gap_eV = 1240.0d0 / absorption_edge_nm

  electron_mobility = 35.0d0
  hole_mobility = 20.0d0
  carrier_lifetime_ns = 650.0d0

  mobility_balance = min(electron_mobility, hole_mobility) / max(electron_mobility, hole_mobility)
  transport_proxy = (electron_mobility + hole_mobility) * carrier_lifetime_ns

  q = 1.602176634d-19
  n = 1.0d16
  p = 1.0d15
  conductivity_proxy = q * (n * electron_mobility + p * hole_mobility)

  print *, "Semiconductor metric kernel"
  print *, "Edge band gap estimate eV:", edge_band_gap_eV
  print *, "Mobility balance:", mobility_balance
  print *, "Transport proxy:", transport_proxy
  print *, "Conductivity proxy:", conductivity_proxy
  print *, "Responsible-use note: synthetic educational calculation only."
end program semiconductor_metric_kernel
