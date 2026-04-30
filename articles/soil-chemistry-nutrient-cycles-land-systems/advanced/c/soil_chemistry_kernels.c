/*
Soil Chemistry, Nutrient Cycles, and Land Systems
C soil chemistry kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double ph_stress(double pH) {
    if (pH < 6.0) return clamp01((6.0 - pH) / 2.0);
    if (pH > 7.8) return clamp01((pH - 7.8) / 2.0);
    return 0.0;
}

double nutrient_balance_index(double nitrate, double ammonium, double available_p, double exchangeable_k) {
    double nitrogen = clamp01((nitrate + ammonium) / 60.0);
    double phosphorus = clamp01(available_p / 40.0);
    double potassium = clamp01(exchangeable_k / 250.0);

    return clamp01(0.40 * nitrogen + 0.30 * phosphorus + 0.30 * potassium);
}

double salinity_sodicity_pressure(double ec_dS_m, double sar) {
    double salinity = clamp01((ec_dS_m - 2.0) / 6.0);
    double sodicity = clamp01((sar - 6.0) / 12.0);
    return salinity > sodicity ? salinity : sodicity;
}

double organic_matter_score(double organic_matter_percent) {
    return clamp01(organic_matter_percent / 6.0);
}

double cec_buffering_score(double cec_cmol_kg) {
    return clamp01(cec_cmol_kg / 25.0);
}

double leaching_pressure(double sand_fraction, double rainfall_index, double nitrate, double cec, double organic_matter) {
    double buffering = 0.5 * cec_buffering_score(cec) + 0.5 * organic_matter_score(organic_matter);
    return clamp01(0.40 * sand_fraction + 0.35 * rainfall_index + 0.25 * clamp01(nitrate / 50.0) - 0.25 * buffering);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_soil_chemistry_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_soil_chemistry_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,pH_stress,nutrient_balance_index,salinity_sodicity_pressure,organic_matter_score,cec_buffering_score,leaching_pressure\n");

    fprintf(fp, "prairie_cropland,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        ph_stress(6.4),
        nutrient_balance_index(18.0, 6.0, 28.0, 190.0),
        salinity_sodicity_pressure(0.8, 2.0),
        organic_matter_score(4.8),
        cec_buffering_score(22.0),
        leaching_pressure(0.28, 0.55, 18.0, 22.0, 4.8)
    );

    fprintf(fp, "irrigated_salinity,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        ph_stress(8.2),
        nutrient_balance_index(25.0, 5.0, 32.0, 210.0),
        salinity_sodicity_pressure(5.8, 12.0),
        organic_matter_score(1.6),
        cec_buffering_score(14.0),
        leaching_pressure(0.44, 0.40, 25.0, 14.0, 1.6)
    );

    fclose(fp);
    printf("C soil chemistry kernels complete.\n");
    return 0;
}
