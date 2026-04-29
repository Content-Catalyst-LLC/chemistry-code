program checksum_sensitivity
  implicit none

  character(len=512) :: path
  character(len=1) :: ch
  integer :: unit_number, ios
  integer(kind=8) :: checksum
  integer(kind=8) :: byte_count

  path = "../data/synthetic_chemical_notebook_runs.csv"
  checksum = 1469598103934665603_8
  byte_count = 0_8

  open(newunit=unit_number, file=trim(path), status="old", action="read", access="stream", iostat=ios)

  if (ios /= 0) then
     print *, "Could not open data file: ", trim(path)
     stop 1
  end if

  do
     read(unit_number, iostat=ios) ch
     if (ios /= 0) exit
     checksum = ieor(checksum, int(iachar(ch), kind=8))
     checksum = checksum * 1099511628211_8
     byte_count = byte_count + 1_8
  end do

  close(unit_number)

  print *, "Synthetic chemical notebook data checksum audit"
  print *, "Bytes read: ", byte_count
  print *, "FNV-like checksum: ", checksum
  print *, "Responsible-use note: synthetic educational data only."
end program checksum_sensitivity
