! Chemistry, Ethics, and the Governance of Molecular Power
! Fortran governance gap scenario model.
! Synthetic educational code only.

program governance_gap_scenario
  implicit none

  integer :: unit_number, step
  real :: risk, governance_strength, gap

  risk = 0.62

  open(newunit=unit_number, file="../outputs/tables/fortran_governance_gap_scenario.csv", status="replace", action="write")
  write(unit_number, '(A)') "step,governance_strength,governance_gap"

  do step = 0, 10
    governance_strength = real(step) / 10.0
    gap = risk * (1.0 - governance_strength)
    write(unit_number, '(I0,A,F12.6,A,F12.6)') step, ",", governance_strength, ",", gap
  end do

  close(unit_number)
  print *, "Fortran governance gap scenario complete."

end program governance_gap_scenario
