/*
Geochemistry and the Chemical History of Earth
C isotope, weathering, and redox kernels.
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

double half_life_ma(const char *parent) {
    if (strcmp(parent, "Rb87") == 0) return 48800.0;
    if (strcmp(parent, "Sm147") == 0) return 106000.0;
    if (strcmp(parent, "K40") == 0) return 1250.0;
    if (strcmp(parent, "U238") == 0) return 4468.0;
    return 0.0;
}

double decay_constant(double half_life) {
    if (half_life <= 0.0) return 0.0;
    return log(2.0) / half_life;
}

double model_age_from_parent_fraction(double parent_fraction, double half_life) {
    if (parent_fraction <= 0.0 || parent_fraction > 1.0 || half_life <= 0.0) return 0.0;
    return -log(parent_fraction) / decay_constant(half_life);
}

double chemical_index_of_alteration(double al2o3, double cao, double na2o, double k2o) {
    double denominator = al2o3 + cao + na2o + k2o;
    if (denominator <= 0.0) return 0.0;
    return 100.0 * al2o3 / denominator;
}

double mafic_index(double mgo, double feo, double tio2, double sio2) {
    double mafic = mgo + feo + tio2;
    double total = mafic + sio2;
    if (total <= 0.0) return 0.0;
    return mafic / total;
}

double rb_sr_ratio(double rb, double sr) {
    if (sr <= 0.0) return 0.0;
    return rb / sr;
}

double redox_state_proxy(double redox_proxy, double feo, double mno) {
    return clamp01(0.65 * redox_proxy + 0.25 * clamp01(feo / 15.0) + 0.10 * clamp01(mno / 0.30));
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_geochemistry_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_geochemistry_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "sample,parent_isotope,half_life_ma,model_age_ma,CIA,mafic_index,Rb_Sr,redox_state_proxy\n");

    fprintf(fp, "superior_granite,Rb87,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        half_life_ma("Rb87"),
        model_age_from_parent_fraction(0.72, half_life_ma("Rb87")),
        chemical_index_of_alteration(14.1, 1.8, 3.4, 4.8),
        mafic_index(0.6, 1.9, 0.31, 72.5),
        rb_sr_ratio(185.0, 210.0),
        redox_state_proxy(0.32, 1.9, 0.04)
    );

    fprintf(fp, "banded_iron_formation,U238,%.8f,%.8f,%.8f,%.8f,%.8f,%.8f\n",
        half_life_ma("U238"),
        model_age_from_parent_fraction(0.61, half_life_ma("U238")),
        chemical_index_of_alteration(2.5, 3.2, 0.1, 0.05),
        mafic_index(2.8, 42.0, 0.2, 38.0),
        rb_sr_ratio(1.0, 22.0),
        redox_state_proxy(0.92, 42.0, 0.25)
    );

    fclose(fp);
    printf("C geochemistry kernels complete.\n");
    return 0;
}
