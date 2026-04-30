/*
Chemistry, Classification, and the Human Understanding of Matter
C chemical classification kernels.
Synthetic educational code only.
*/

#include <stdio.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double evidence_score(double spectral, double elemental, double thermal, double qc) {
    return clamp01(0.35 * spectral + 0.30 * elemental + 0.20 * thermal + 0.15 * qc);
}

double classification_reliability(double evidence, double confidence, double qc) {
    return clamp01(0.55 * evidence + 0.30 * confidence + 0.15 * qc);
}

double materiality_score(double crystalline, double network_structure, double polymer, double metallic_fraction) {
    return clamp01(0.30 * crystalline + 0.30 * network_structure + 0.25 * polymer + 0.15 * metallic_fraction);
}

double mixture_complexity_score(double components, double organic_fraction, double ionic_fraction) {
    double component_score = clamp01(components / 20.0);
    return clamp01(0.60 * component_score + 0.20 * organic_fraction + 0.20 * ionic_fraction);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_chemical_classification_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_chemical_classification_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    double e1 = evidence_score(0.92, 0.88, 0.74, 0.94);
    double e2 = evidence_score(0.48, 0.72, 0.55, 0.82);

    fprintf(fp, "record,evidence_score,classification_reliability,materiality_score,mixture_complexity_score\n");
    fprintf(fp, "ethyl_acetate_reference,%.8f,%.8f,%.8f,%.8f\n",
        e1,
        classification_reliability(e1, 0.86, 0.94),
        materiality_score(0.05, 0.0, 0.0, 0.0),
        mixture_complexity_score(1.0, 1.0, 0.0)
    );

    fprintf(fp, "soil_extract,%.8f,%.8f,%.8f,%.8f\n",
        e2,
        classification_reliability(e2, 0.60, 0.82),
        materiality_score(0.42, 1.0, 0.0, 0.05),
        mixture_complexity_score(60.0, 0.30, 0.50)
    );

    fclose(fp);
    printf("C chemical classification kernels complete.\n");
    return 0;
}
