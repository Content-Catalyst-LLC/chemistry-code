#include <math.h>
#include <stdio.h>

/*
Ocean carbonate chemistry pH and carbonate-fraction example.

Educational only. Real seawater carbonate calculations require
temperature-, salinity-, pressure-, nutrient-, and pH-scale-dependent constants.
*/

double carbonate_alpha2(double pH) {
    double K1 = pow(10.0, -6.0);
    double K2 = pow(10.0, -9.1);
    double H = pow(10.0, -pH);
    double denominator = H * H + K1 * H + K1 * K2;
    return K1 * K2 / denominator;
}

double hydrogen_concentration(double pH) {
    return pow(10.0, -pH);
}

int main(void) {
    double pH_values[] = {8.10, 7.78, 8.02, 7.62};

    printf("case,pH,H_mol_L_simplified,alpha_CO3\n");

    for (int i = 0; i < 4; i++) {
        double pH = pH_values[i];
        printf(
            "%d,%.3f,%.8e,%.8e\n",
            i + 1,
            pH,
            hydrogen_concentration(pH),
            carbonate_alpha2(pH)
        );
    }

    return 0;
}
