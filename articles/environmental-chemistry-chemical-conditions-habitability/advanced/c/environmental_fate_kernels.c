/*
Environmental Chemistry and the Chemical Conditions of Habitability
C fate and transport kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double kd_l_kg(double koc_l_kg, double organic_carbon_fraction) {
    return koc_l_kg * organic_carbon_fraction;
}

double retardation_factor(double kd, double bulk_density_g_cm3, double porosity) {
    if (porosity < 0.01) porosity = 0.01;
    return 1.0 + (bulk_density_g_cm3 * kd) / porosity;
}

double mobility_factor(double retardation) {
    if (retardation < 1.0) retardation = 1.0;
    return 1.0 / sqrt(retardation);
}

double henry_tendency(double henry_atm_m3_mol) {
    double x = log1p(fmax(henry_atm_m3_mol, 0.0) * 1000.0) / log(20.0);
    return clamp01(x);
}

double first_order_decay_constant(double half_life_days) {
    if (half_life_days <= 0.0) return 0.0;
    return log(2.0) / half_life_days;
}

double concentration_after_time(double c0, double half_life_days, double days) {
    double k = first_order_decay_constant(half_life_days);
    return c0 * exp(-k * days);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_environmental_fate_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_environmental_fate_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,Kd_L_kg,retardation_factor,mobility_factor,henry_tendency,decay_constant_per_day,concentration_day_365\n");

    double kd = kd_l_kg(90.0, 0.001);
    double r = retardation_factor(kd, 1.70, 0.30);

    fprintf(fp, "TCE_groundwater,%.8f,%.8f,%.8f,%.8f,%.10f,%.8f\n",
        kd,
        r,
        mobility_factor(r),
        henry_tendency(0.0091),
        first_order_decay_constant(365.0),
        concentration_after_time(8.5, 365.0, 365.0)
    );

    kd = kd_l_kg(60000.0, 0.055);
    r = retardation_factor(kd, 1.15, 0.58);

    fprintf(fp, "pyrene_sediment,%.8f,%.8f,%.8f,%.8f,%.10f,%.8f\n",
        kd,
        r,
        mobility_factor(r),
        henry_tendency(0.0000012),
        first_order_decay_constant(220.0),
        concentration_after_time(1.9, 220.0, 365.0)
    );

    fclose(fp);
    printf("C environmental fate kernels complete.\n");
    return 0;
}
