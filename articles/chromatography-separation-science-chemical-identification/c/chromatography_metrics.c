#include <stdio.h>

int main(void) {
    double tM = 0.92;
    double tR_A = 2.85;
    double tR_B = 4.10;
    double w_A = 0.25;
    double w_B = 0.31;

    double k_A = (tR_A - tM) / tM;
    double k_B = (tR_B - tM) / tM;
    double alpha = k_B / k_A;
    double resolution = 2.0 * (tR_B - tR_A) / (w_A + w_B);

    printf("Chromatography metric utility\n");
    printf("Retention factor A: %.6f\n", k_A);
    printf("Retention factor B: %.6f\n", k_B);
    printf("Selectivity alpha: %.6f\n", alpha);
    printf("Resolution Rs: %.6f\n", resolution);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
