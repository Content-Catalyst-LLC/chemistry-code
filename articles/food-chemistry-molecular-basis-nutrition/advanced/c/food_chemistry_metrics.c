/*
Food Chemistry and the Molecular Basis of Nutrition
C nutrient-density and lipid-oxidation example.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double nutrient_density(double protein_g, double fiber_g, double potassium_mg, double energy_kcal) {
    double beneficial =
        0.40 * clamp01(protein_g / 25.0) +
        0.35 * clamp01(fiber_g / 12.0) +
        0.25 * clamp01(potassium_mg / 800.0);

    double energy_factor = energy_kcal / 100.0;
    if (energy_factor < 0.5) energy_factor = 0.5;

    return beneficial / energy_factor;
}

double lipid_oxidation_vulnerability(double total_fat_g, double unsaturation_index, double antioxidant_protection, double processing_intensity) {
    if (total_fat_g <= 0.0) return 0.0;

    return clamp01(
        0.45 * clamp01(unsaturation_index / 4.5) +
        0.25 * processing_intensity -
        0.30 * antioxidant_protection
    );
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_food_chemistry_metrics.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_food_chemistry_metrics.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "food,nutrient_density,lipid_oxidation_vulnerability\n");
    fprintf(fp, "lentils_cooked,%.6f,%.6f\n",
        nutrient_density(18.0, 15.0, 730.0, 230.0),
        lipid_oxidation_vulnerability(1.0, 0.55, 0.75, 0.25)
    );
    fprintf(fp, "walnuts,%.6f,%.6f\n",
        nutrient_density(15.0, 7.0, 320.0, 330.0),
        lipid_oxidation_vulnerability(32.0, 4.20, 0.88, 0.20)
    );

    fclose(fp);
    printf("C food chemistry metrics complete.\n");
    return 0;
}
