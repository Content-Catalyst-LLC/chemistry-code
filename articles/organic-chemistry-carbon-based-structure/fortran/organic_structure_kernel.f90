program organic_structure_kernel
  implicit none

  real(8) :: benzene_dbe, acetic_acid_dbe, polarity_score

  benzene_dbe = 6.0d0 - (6.0d0 + 0.0d0) / 2.0d0 + 0.0d0 / 2.0d0 + 1.0d0
  acetic_acid_dbe = 2.0d0 - (4.0d0 + 0.0d0) / 2.0d0 + 0.0d0 / 2.0d0 + 1.0d0
  polarity_score = 2.0d0 + 1.0d0 + 2.0d0

  print *, "benzene_DBE=", benzene_dbe
  print *, "acetic_acid_DBE=", acetic_acid_dbe
  print *, "polarity_score=", polarity_score

end program organic_structure_kernel
