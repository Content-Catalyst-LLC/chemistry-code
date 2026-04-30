! Chemistry, Classification, and the Human Understanding of Matter
! Fortran feature-space similarity scenario.
! Synthetic educational code only.

program classification_similarity
  implicit none

  integer :: unit_number
  real :: d1, d2, d3

  d1 = euclidean_distance(0.92, 0.88, 0.74, 0.90, 0.84, 0.72)
  d2 = euclidean_distance(0.70, 0.82, 0.40, 0.60, 0.78, 0.50)
  d3 = euclidean_distance(0.48, 0.72, 0.55, 0.86, 0.88, 0.70)

  open(newunit=unit_number, file="../outputs/tables/fortran_classification_similarity.csv", status="replace", action="write")
  write(unit_number, '(A)') "comparison,distance"
  write(unit_number, '(A,F12.6)') "organic_reference_vs_candidate,", d1
  write(unit_number, '(A,F12.6)') "solution_reference_vs_candidate,", d2
  write(unit_number, '(A,F12.6)') "mixed_matrix_vs_candidate,", d3
  close(unit_number)

  print *, "Fortran classification similarity model complete."

contains

  real function euclidean_distance(a1, a2, a3, b1, b2, b3)
    real, intent(in) :: a1, a2, a3, b1, b2, b3
    euclidean_distance = sqrt((a1 - b1)**2 + (a2 - b2)**2 + (a3 - b3)**2)
  end function euclidean_distance

end program classification_similarity
