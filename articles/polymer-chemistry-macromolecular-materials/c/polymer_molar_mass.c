#include <stdio.h>

int main(void) {
    double counts[5] = {1000.0, 1800.0, 2400.0, 1600.0, 700.0};
    double masses[5] = {25000.0, 55000.0, 90000.0, 135000.0, 210000.0};

    double sum_counts = 0.0;
    double sum_nm = 0.0;
    double sum_nm2 = 0.0;

    for (int i = 0; i < 5; i++) {
        sum_counts += counts[i];
        sum_nm += counts[i] * masses[i];
        sum_nm2 += counts[i] * masses[i] * masses[i];
    }

    double Mn = sum_nm / sum_counts;
    double Mw = sum_nm2 / sum_nm;
    double dispersity = Mw / Mn;

    printf("Polymer molar-mass utility\n");
    printf("Mn g/mol: %.6f\n", Mn);
    printf("Mw g/mol: %.6f\n", Mw);
    printf("Dispersity: %.6f\n", dispersity);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
