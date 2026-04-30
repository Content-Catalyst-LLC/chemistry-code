/*
Green Chemistry, Responsibility, and Sustainable Transformation
C green chemistry metric kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double atom_economy(double product_mw, double reactant_mw_sum) {
    if (reactant_mw_sum <= 0.0) return 0.0;
    return product_mw / reactant_mw_sum;
}

double e_factor(double waste_mass, double product_mass) {
    if (product_mass <= 0.0) return 0.0;
    return waste_mass / product_mass;
}

double process_mass_intensity(double total_input_mass, double product_mass) {
    if (product_mass <= 0.0) return 0.0;
    return total_input_mass / product_mass;
}

double hazard_weighted_mass_intensity(double pmi, double hazard_score, double solvent_hazard_score) {
    return pmi * (0.60 * hazard_score + 0.40 * solvent_hazard_score);
}

double catalysis_score(double catalyst_loading_mol_percent) {
    if (catalyst_loading_mol_percent <= 0.0) return 0.0;
    return clamp01(1.0 - catalyst_loading_mol_percent / 20.0);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_green_chemistry_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_green_chemistry_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "route,atom_economy,e_factor,pmi,hazard_weighted_mass_intensity,catalysis_score\n");

    double pmi_a = process_mass_intensity(36.0, 2.0);
    fprintf(fp, "Route_A_Stoichiometric,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        atom_economy(180.0, 260.0),
        e_factor(28.0, 2.0),
        pmi_a,
        hazard_weighted_mass_intensity(pmi_a, 0.55, 0.62),
        catalysis_score(0.0)
    );

    double pmi_b = process_mass_intensity(18.0, 2.4);
    fprintf(fp, "Route_B_Catalytic,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        atom_economy(180.0, 225.0),
        e_factor(10.0, 2.4),
        pmi_b,
        hazard_weighted_mass_intensity(pmi_b, 0.30, 0.35),
        catalysis_score(2.0)
    );

    fclose(fp);
    printf("C green chemistry kernels complete.\n");
    return 0;
}
