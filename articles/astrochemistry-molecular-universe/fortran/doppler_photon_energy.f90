program doppler_photon_energy
  implicit none

  real(8), parameter :: c_km_s = 299792.458d0
  real(8), parameter :: h_j_s = 6.62607015d-34
  real(8) :: rest_ghz, obs_ghz, velocity, energy
  integer :: i
  character(len=*), parameter :: outfile = "../outputs/tables/fortran_doppler_photon_energy.csv"

  real(8), dimension(4) :: rest_values = (/115.271d0, 96.741d0, 88.632d0, 556.936d0/)
  real(8), dimension(4) :: obs_values = (/115.269d0, 96.738d0, 88.631d0, 556.920d0/)

  open(unit=10, file=outfile, status="replace", action="write")
  write(10, '(A)') "case,rest_frequency_GHz,observed_frequency_GHz,radial_velocity_km_s,photon_energy_J"

  do i = 1, 4
     rest_ghz = rest_values(i)
     obs_ghz = obs_values(i)
     velocity = -c_km_s * (obs_ghz - rest_ghz) / rest_ghz
     energy = h_j_s * rest_ghz * 1.0d9

     write(10, '(I0,A,F12.6,A,F12.6,A,F12.6,A,ES14.6)') i, ",", rest_ghz, ",", obs_ghz, ",", velocity, ",", energy
  end do

  close(10)
  print *, "Doppler velocity and photon energy calculations complete."
end program doppler_photon_energy
