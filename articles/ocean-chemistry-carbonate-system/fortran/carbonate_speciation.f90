program carbonate_speciation
  implicit none

  real(8) :: pH, H, K1, K2, denom, alpha0, alpha1, alpha2
  integer :: i
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_carbonate_fractions.csv"
  real(8), dimension(4) :: ph_values = (/8.10d0, 7.78d0, 8.02d0, 7.62d0/)

  K1 = 10.0d0 ** (-6.0d0)
  K2 = 10.0d0 ** (-9.1d0)

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "case,pH,alpha_CO2_star,alpha_HCO3,alpha_CO3"

  do i = 1, 4
     pH = ph_values(i)
     H = 10.0d0 ** (-pH)
     denom = H**2 + K1 * H + K1 * K2
     alpha0 = H**2 / denom
     alpha1 = K1 * H / denom
     alpha2 = K1 * K2 / denom

     write(10, '(I0,A,F8.3,A,ES14.6,A,ES14.6,A,ES14.6)') i, ",", pH, ",", alpha0, ",", alpha1, ",", alpha2
  end do

  close(10)

  print *, "Simplified carbonate speciation calculation complete."
end program carbonate_speciation
