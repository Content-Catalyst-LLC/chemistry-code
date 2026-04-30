/*
Atmospheric Chemistry and Climate Processes
C radiative forcing, ozone, aerosol, and persistence kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>
#include <string.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double reference_ratio(double concentration, double reference) {
    if (reference <= 0.0) return 0.0;
    return concentration / reference;
}

double greenhouse_forcing_proxy(const char *species, double concentration, double reference) {
    if (concentration <= 0.0 || reference <= 0.0) return 0.0;

    if (strcmp(species, "CO2") == 0) {
        return 5.35 * log(concentration / reference);
    }

    if (strcmp(species, "CH4") == 0) {
        return 0.036 * (sqrt(concentration) - sqrt(reference));
    }

    if (strcmp(species, "N2O") == 0) {
        return 0.12 * (sqrt(concentration) - sqrt(reference));
    }

    return 0.0;
}

double photochemical_ozone_index(double nox_ppb, double voc_ppb, double sunlight_index) {
    if (nox_ppb <= 0.0 || voc_ppb <= 0.0) return 0.0;
    return sqrt(nox_ppb * voc_ppb) * sunlight_index;
}

double aerosol_direct_effect_proxy(double aod, double single_scattering_albedo) {
    double scattering = -25.0 * aod * single_scattering_albedo;
    double absorption = 12.0 * aod * (1.0 - single_scattering_albedo);
    return scattering + absorption;
}

double persistence_factor(double lifetime_days) {
    return lifetime_days / (lifetime_days + 30.0);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_atmospheric_chemistry_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_atmospheric_chemistry_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,species,reference_ratio,forcing_proxy,ozone_index,aerosol_effect,persistence_factor\n");

    fprintf(fp, "co2_background,CO2,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        reference_ratio(423.0, 280.0),
        greenhouse_forcing_proxy("CO2", 423.0, 280.0),
        photochemical_ozone_index(0.0, 0.0, 1.0),
        aerosol_direct_effect_proxy(0.04, 0.96),
        persistence_factor(36500.0)
    );

    fprintf(fp, "urban_ozone,O3,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        reference_ratio(0.078, 0.070),
        greenhouse_forcing_proxy("O3", 0.078, 0.070),
        photochemical_ozone_index(38.0, 85.0, 1.15),
        aerosol_direct_effect_proxy(0.08, 0.93),
        persistence_factor(0.20)
    );

    fprintf(fp, "wildfire_pm,PM2.5,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        reference_ratio(38.0, 15.0),
        greenhouse_forcing_proxy("PM2.5", 38.0, 15.0),
        photochemical_ozone_index(22.0, 95.0, 0.75),
        aerosol_direct_effect_proxy(0.68, 0.86),
        persistence_factor(5.0)
    );

    fclose(fp);
    printf("C atmospheric chemistry kernels complete.\n");
    return 0;
}
