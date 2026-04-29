program workflow_reliability_kernel
  implicit none

  real(8) :: scheduled, completed, failed, metadata_present, metadata_required
  real(8) :: completion_fraction, failure_fraction, metadata_completeness

  scheduled = 8.0d0
  completed = 7.0d0
  failed = 1.0d0
  metadata_present = 86.0d0
  metadata_required = 90.0d0

  completion_fraction = completed / scheduled
  failure_fraction = failed / scheduled
  metadata_completeness = metadata_present / metadata_required

  print *, "Laboratory automation reliability kernel"
  print *, "Completion fraction:", completion_fraction
  print *, "Failure fraction:", failure_fraction
  print *, "Metadata completeness:", metadata_completeness
  print *, "Responsible-use note: synthetic educational calculation only."
end program workflow_reliability_kernel
