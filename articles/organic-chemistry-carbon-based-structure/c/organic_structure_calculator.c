#include <stdio.h>

double dbe(double c, double h, double n, double x) {
    return c - (h + x) / 2.0 + n / 2.0 + 1.0;
}

double polarity_score(double heteroatoms, double donors, double acceptors) {
    return heteroatoms + donors + acceptors;
}

int main(void) {
    printf("benzene_DBE=%.6f\n", dbe(6.0, 6.0, 0.0, 0.0));
    printf("acetic_acid_DBE=%.6f\n", dbe(2.0, 4.0, 0.0, 0.0));
    printf("polarity_score=%.6f\n", polarity_score(2.0, 1.0, 2.0));
    return 0;
}
