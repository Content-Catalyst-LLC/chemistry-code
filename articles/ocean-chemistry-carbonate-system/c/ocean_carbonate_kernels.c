/*
Ocean Chemistry and the Carbonate System
C carbonate chemistry proxy kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double hydrogen_ion_from_pH(double pH) {
    return pow(10.0, -pH);
}

double alkalinity_dic_ratio(double alkalinity, double dic) {
    if (dic <= 0.0) return 0.0;
    return alkalinity / dic;
}

double carbonate_buffer_proxy(double pH, double alkalinity, double dic) {
    double ratio = alkalinity_dic_ratio(alkalinity, dic);
    double pH_component = clamp01((pH - 7.6) / 0.7);
    double ratio_component = clamp01((ratio - 1.0) / 0.20);
    return clamp01(0.55 * pH_component + 0.45 * ratio_component);
}

double saturation_proxy(double carbonate_umol_kg, double calcium_mmol_kg, double ksp_proxy) {
    double calcium_umol_kg = calcium_mmol_kg * 1000.0;
    if (ksp_proxy <= 0.0) return 0.0;
    return (carbonate_umol_kg * calcium_umol_kg) / (ksp_proxy * 100000.0);
}

double acidification_pressure(double pH, double pco2, double carbonate_umol_kg, double omega_aragonite) {
    double pH_component = clamp01((8.2 - pH) / 0.7);
    double co2_component = clamp01((pco2 - 400.0) / 800.0);
    double carbonate_component = clamp01((180.0 - carbonate_umol_kg) / 180.0);
    double saturation_component = clamp01((3.0 - omega_aragonite) / 3.0);

    return clamp01(
        0.30 * pH_component +
        0.25 * co2_component +
        0.25 * carbonate_component +
        0.20 * saturation_component
    );
}

double deoxygenation_pressure(double oxygen_umol_kg) {
    return clamp01((180.0 - oxygen_umol_kg) / 180.0);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_ocean_carbonate_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_ocean_carbonate_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,pH,H_plus,alkalinity_dic_ratio,buffer_proxy,omega_aragonite,acidification_pressure,deoxygenation_pressure\n");

    double omega = saturation_proxy(145.0, 10.2, 60.0);
    fprintf(fp, "equatorial_pacific,%.4f,%.12f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        7.92,
        hydrogen_ion_from_pH(7.92),
        alkalinity_dic_ratio(2285.0, 2130.0),
        carbonate_buffer_proxy(7.92, 2285.0, 2130.0),
        omega,
        acidification_pressure(7.92, 520.0, 145.0, omega),
        deoxygenation_pressure(210.0)
    );

    omega = saturation_proxy(62.0, 10.2, 60.0);
    fprintf(fp, "arabian_sea_omz,%.4f,%.12f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        7.62,
        hydrogen_ion_from_pH(7.62),
        alkalinity_dic_ratio(2320.0, 2265.0),
        carbonate_buffer_proxy(7.62, 2320.0, 2265.0),
        omega,
        acidification_pressure(7.62, 1050.0, 62.0, omega),
        deoxygenation_pressure(18.0)
    );

    fclose(fp);
    printf("C ocean carbonate kernels complete.\n");
    return 0;
}
