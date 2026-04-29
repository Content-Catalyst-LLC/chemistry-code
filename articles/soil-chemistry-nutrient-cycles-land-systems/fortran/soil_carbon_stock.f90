program soil_carbon_stock
  implicit none

  real(8) :: soc_percent, bulk_density, depth_cm, stock
  integer :: i
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_soil_carbon_stock.csv"

  real(8), dimension(3) :: soc_values = (/1.8d0, 7.5d0, 4.1d0/)
  real(8), dimension(3) :: bd_values = (/1.32d0, 0.82d0, 1.05d0/)
  real(8), dimension(3) :: depth_values = (/30.0d0, 30.0d0, 30.0d0/)

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "case,soc_percent,bulk_density_g_cm3,depth_cm,soc_stock_Mg_ha"

  do i = 1, 3
     soc_percent = soc_values(i)
     bulk_density = bd_values(i)
     depth_cm = depth_values(i)
     stock = soc_percent * bulk_density * depth_cm
     write(10, '(I0,A,F8.3,A,F8.3,A,F8.3,A,F10.4)') i, ",", soc_percent, ",", bulk_density, ",", depth_cm, ",", stock
  end do

  close(10)
  print *, "Soil organic carbon stock calculation complete."
end program soil_carbon_stock
