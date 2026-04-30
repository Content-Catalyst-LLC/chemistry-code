/*
Water Chemistry and Environmental Monitoring
C water-quality kernels.
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

double benchmark_ratio(double concentration, double benchmark) {
    if (benchmark <= 0.0) return 0.0;
    return concentration / benchmark;
}

double load_kg_day(double concentration, const char *unit, double flow_l_s) {
    if (flow_l_s <= 0.0) return 0.0;

    if (strcmp(unit, "mg/L") == 0) {
        return concentration * flow_l_s * 0.0864;
    }

    if (strcmp(unit, "ug/L") == 0) {
        return concentration * flow_l_s * 0.0000864;
    }

    return 0.0;
}

double oxygen_deficit(double dissolved_oxygen_mg_l, double saturation_mg_l) {
    double deficit = saturation_mg_l - dissolved_oxygen_mg_l;
    return deficit > 0.0 ? deficit : 0.0;
}

double oxygen_stress(double dissolved_oxygen_mg_l, double saturation_mg_l) {
    double low_do = clamp01((6.0 - dissolved_oxygen_mg_l) / 6.0);
    double deficit = clamp01(oxygen_deficit(dissolved_oxygen_mg_l, saturation_mg_l) / 6.0);
    return clamp01(0.60 * low_do + 0.40 * deficit);
}

double nutrient_index(double nitrate_mg_l, double phosphate_mg_l) {
    return clamp01(0.50 * clamp01(nitrate_mg_l / 10.0) +
                   0.50 * clamp01(phosphate_mg_l / 0.20));
}

double metal_index(double lead_ug_l, double copper_ug_l, double arsenic_ug_l) {
    return clamp01(
        0.34 * clamp01(lead_ug_l / 15.0) +
        0.33 * clamp01(copper_ug_l / 13.0) +
        0.33 * clamp01(arsenic_ug_l / 10.0)
    );
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_water_quality_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_water_quality_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,benchmark_ratio,load_kg_day,oxygen_deficit,oxygen_stress,nutrient_index,metal_index\n");

    fprintf(fp, "river_nitrate,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        benchmark_ratio(7.8, 10.0),
        load_kg_day(7.8, "mg/L", 820.0),
        oxygen_deficit(8.2, 10.2),
        oxygen_stress(8.2, 10.2),
        nutrient_index(7.8, 0.18),
        metal_index(3.0, 5.0, 2.5)
    );

    fprintf(fp, "stormwater_lead,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        benchmark_ratio(18.0, 15.0),
        load_kg_day(18.0, "ug/L", 210.0),
        oxygen_deficit(6.4, 9.1),
        oxygen_stress(6.4, 9.1),
        nutrient_index(4.5, 0.42),
        metal_index(18.0, 21.0, 3.0)
    );

    fclose(fp);
    printf("C water quality kernels complete.\n");
    return 0;
}
