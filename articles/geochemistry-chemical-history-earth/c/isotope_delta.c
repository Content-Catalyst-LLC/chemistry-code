#include <stdio.h>

/*
Isotope delta notation example.

delta = ((R_sample / R_standard) - 1) * 1000

Educational only. Real isotope workflows require standards, normalization,
instrument correction, uncertainty, and laboratory QA/QC.
*/

double isotope_delta(double sample_ratio, double standard_ratio) {
    return ((sample_ratio / standard_ratio) - 1.0) * 1000.0;
}

int main(void) {
    double carbon_sample = 0.01112;
    double carbon_standard = 0.01118;

    double oxygen_sample = 0.002021;
    double oxygen_standard = 0.0020052;

    printf("system,sample_ratio,standard_ratio,delta_permil\n");
    printf("carbon,%.8f,%.8f,%.4f\n", carbon_sample, carbon_standard, isotope_delta(carbon_sample, carbon_standard));
    printf("oxygen,%.8f,%.8f,%.4f\n", oxygen_sample, oxygen_standard, isotope_delta(oxygen_sample, oxygen_standard));

    return 0;
}
