#include <math.h>
#include <stdio.h>

// Compact normalized-error kernel for interlaboratory comparison.

int main(void) {
    double x_lab = 10.2;
    double x_ref = 10.0;
    double u_lab = 0.8;
    double u_ref = 0.4;

    double en = (x_lab - x_ref) / sqrt(u_lab * u_lab + u_ref * u_ref);

    printf("normalized_error=%.6f\n", en);

    return 0;
}
