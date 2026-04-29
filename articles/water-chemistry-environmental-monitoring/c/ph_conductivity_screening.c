#include <stdio.h>

/*
Water chemistry field-parameter screening example.

Educational only. pH and conductivity thresholds are illustrative and not
regulatory determinations.
*/

const char* ph_flag(double ph) {
    if (ph < 6.5 || ph > 9.0) {
        return "outside_illustrative_aquatic_range";
    }
    return "within_illustrative_aquatic_range";
}

const char* conductivity_flag(double conductivity_us_cm) {
    if (conductivity_us_cm > 1000.0) {
        return "elevated_conductivity_screen";
    }
    return "not_elevated_screen";
}

int main(void) {
    const char* sites[] = {"River-A", "Lake-B", "Mine-F"};
    double ph_values[] = {7.4, 8.6, 5.2};
    double conductivity[] = {640.0, 420.0, 1450.0};

    printf("site,pH,pH_flag,conductivity_uS_cm,conductivity_flag\n");

    for (int i = 0; i < 3; i++) {
        printf(
            "%s,%.2f,%s,%.1f,%s\n",
            sites[i],
            ph_values[i],
            ph_flag(ph_values[i]),
            conductivity[i],
            conductivity_flag(conductivity[i])
        );
    }

    return 0;
}
