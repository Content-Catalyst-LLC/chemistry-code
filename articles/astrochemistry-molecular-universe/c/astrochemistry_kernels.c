/*
Astrochemistry and the Molecular Universe
C reaction-rate, photodissociation, freeze-out, and attenuation kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double arrhenius_like_rate(double alpha, double activation_k, double temperature_k) {
    if (temperature_k <= 0.0) return 0.0;
    return alpha * exp(-activation_k / temperature_k);
}

double uv_attenuation(double uv_field_g0, double visual_extinction_mag) {
    return uv_field_g0 * exp(-1.8 * visual_extinction_mag);
}

double attenuated_photodissociation_rate(double base_rate_s, double uv_field_g0, double visual_extinction_mag) {
    return base_rate_s * uv_attenuation(uv_field_g0, visual_extinction_mag);
}

double freezeout_efficiency(double density_cm3, double dust_temperature_k, double binding_energy_k) {
    double density_component = clamp01(log10(fmax(density_cm3, 1.0)) / 8.0);
    double thermal_retention = clamp01(binding_energy_k / fmax(100.0 * dust_temperature_k, 1.0));
    return clamp01(0.55 * density_component + 0.45 * thermal_retention);
}

double thermal_desorption_proxy(double binding_energy_k, double dust_temperature_k) {
    if (dust_temperature_k <= 0.0) return 0.0;
    return clamp01(exp(-binding_energy_k / dust_temperature_k) * 1.0e8);
}

double column_abundance_ratio(double species_column, double h2_column) {
    if (h2_column <= 0.0) return 0.0;
    return species_column / h2_column;
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_astrochemistry_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_astrochemistry_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,rate_proxy,uv_attenuation,photo_rate,freezeout_efficiency,thermal_desorption_proxy,column_abundance_ratio\n");

    fprintf(fp, "cold_dark_cloud,%.12e,%.12e,%.12e,%.8f,%.8f,%.12e\n",
        arrhenius_like_rate(2.0e-10, 25.0, 10.0),
        uv_attenuation(0.05, 12.0),
        attenuated_photodissociation_rate(1.0e-11, 0.05, 12.0),
        freezeout_efficiency(120000.0, 8.0, 3600.0),
        thermal_desorption_proxy(3600.0, 8.0),
        column_abundance_ratio(2.2e13, 1.0e22)
    );

    fprintf(fp, "hot_core,%.12e,%.12e,%.12e,%.8f,%.8f,%.12e\n",
        arrhenius_like_rate(8.0e-10, 250.0, 150.0),
        uv_attenuation(10.0, 8.0),
        attenuated_photodissociation_rate(3.0e-10, 10.0, 8.0),
        freezeout_efficiency(5000000.0, 120.0, 4200.0),
        thermal_desorption_proxy(4200.0, 120.0),
        column_abundance_ratio(8.0e15, 1.0e24)
    );

    fclose(fp);
    printf("C astrochemistry kernels complete.\n");
    return 0;
}
