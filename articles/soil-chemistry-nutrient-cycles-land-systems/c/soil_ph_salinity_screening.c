#include <stdio.h>

/*
Soil field-parameter screening example.

Educational only. Thresholds are illustrative and not agronomic,
regulatory, or contamination determinations.
*/

const char* ph_flag(double ph) {
    if (ph < 5.8) {
        return "acidic_screen";
    }
    if (ph > 8.2) {
        return "alkaline_screen";
    }
    return "general_range_screen";
}

const char* salinity_flag(double ec_ds_m) {
    if (ec_ds_m > 1.2) {
        return "elevated_salinity_screen";
    }
    return "not_elevated_screen";
}

int main(void) {
    const char* sites[] = {"Field-A", "Field-B", "Mine-G"};
    double ph_values[] = {6.4, 5.3, 4.8};
    double ec_values[] = {0.42, 0.56, 1.45};

    printf("site,pH,pH_flag,electrical_conductivity_dS_m,salinity_flag\n");

    for (int i = 0; i < 3; i++) {
        printf(
            "%s,%.2f,%s,%.2f,%s\n",
            sites[i],
            ph_values[i],
            ph_flag(ph_values[i]),
            ec_values[i],
            salinity_flag(ec_values[i])
        );
    }

    return 0;
}
