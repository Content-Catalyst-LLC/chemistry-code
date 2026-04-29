#include <stdio.h>
#include <math.h>

int main(void) {
    const double R = 8.314462618;
    const double T = 298.15;
    const double F = 96485.33212;

    double n = 1.0;
    double nernst_slope_v = R * T / (n * F) * log(10.0);

    double blank_sd_uA = 0.002081666;
    double sensitivity_uA_per_uM = 0.0336;
    double lod_uM = 3.0 * blank_sd_uA / sensitivity_uA_per_uM;

    printf("Electrochemical metric utility\n");
    printf("Nernst slope V per decade at 298.15 K: %.8f\n", nernst_slope_v);
    printf("Estimated LOD uM: %.8f\n", lod_uM);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
