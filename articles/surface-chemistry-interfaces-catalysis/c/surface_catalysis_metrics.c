#include <stdio.h>
#include <math.h>

int main(void) {
    double KA = 1.8;
    double KB = 0.7;
    double PA = 1.0;
    double PB = 0.5;
    double Ea = 58.0;
    double R = 0.008314;
    double T = 550.0;
    double Apre = 1.0e5;
    double sites = 120.0;

    double denominator = 1.0 + KA * PA + KB * PB;
    double thetaA = KA * PA / denominator;
    double thetaB = KB * PB / denominator;
    double k = Apre * exp(-Ea / (R * T));
    double rateProxy = k * thetaA * thetaB * sites;

    printf("Surface catalysis metric utility\n");
    printf("theta A: %.8f\n", thetaA);
    printf("theta B: %.8f\n", thetaB);
    printf("rate proxy: %.8f\n", rateProxy);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
