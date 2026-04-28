program limiting_reagent_kernel
  implicit none

  real(8) :: h2_mol, o2_mol
  real(8) :: extent_h2, extent_o2
  real(8) :: maximum_extent
  real(8) :: water_mol, theoretical_yield_g, percent_yield

  h2_mol = 4.0d0
  o2_mol = 1.5d0

  extent_h2 = h2_mol / 2.0d0
  extent_o2 = o2_mol / 1.0d0

  maximum_extent = min(extent_h2, extent_o2)
  water_mol = maximum_extent * 2.0d0
  theoretical_yield_g = water_mol * 18.01528d0
  percent_yield = 45.0d0 / theoretical_yield_g * 100.0d0

  print *, "maximum_extent_mol=", maximum_extent
  print *, "water_mol=", water_mol
  print *, "theoretical_yield_g=", theoretical_yield_g
  print *, "percent_yield=", percent_yield

end program limiting_reagent_kernel
