#include <stdio.h>

int main(void) {
    double scheduled = 8.0;
    double completed = 7.0;
    double failed = 1.0;
    double metadata_present = 86.0;
    double metadata_required = 90.0;

    double completion_fraction = completed / scheduled;
    double failure_fraction = failed / scheduled;
    double metadata_completeness = metadata_present / metadata_required;

    printf("Laboratory automation metric utility\n");
    printf("Completion fraction: %.6f\n", completion_fraction);
    printf("Failure fraction: %.6f\n", failure_fraction);
    printf("Metadata completeness: %.6f\n", metadata_completeness);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
