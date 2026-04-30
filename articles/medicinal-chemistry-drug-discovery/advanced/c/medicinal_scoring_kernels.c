/*
Medicinal Chemistry and Drug Discovery
C scoring kernels for potency, LLE, selectivity, and liability.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double pic50_from_nm(double ic50_nm) {
    return -log10(ic50_nm * 1e-9);
}

double lle(double ic50_nm, double clogp) {
    return pic50_from_nm(ic50_nm) - clogp;
}

double selectivity_window(double off_target_ic50_nm, double target_ic50_nm) {
    if (target_ic50_nm <= 0.0) return 0.0;
    return off_target_ic50_nm / target_ic50_nm;
}

double herg_risk(double herg_ic50_um) {
    return clamp01((10.0 - herg_ic50_um) / 10.0);
}

double cyp_risk(double cyp_ic50_um) {
    return clamp01((20.0 - cyp_ic50_um) / 20.0);
}

double mpo_score(double ic50_nm, double off_target_ic50_nm, double clogp, double solubility_um, double permeability, double herg_ic50_um, double cyp_ic50_um, double qc) {
    double potency = clamp01((pic50_from_nm(ic50_nm) - 5.0) / 3.0);
    double selectivity = clamp01(log10(fmax(selectivity_window(off_target_ic50_nm, ic50_nm), 1.0)) / 3.0);
    double lle_score = clamp01((lle(ic50_nm, clogp) - 2.0) / 5.0);
    double solubility_score = clamp01(log10(fmax(solubility_um, 0.001)) / 2.3);
    double permeability_score = clamp01(permeability / 30.0);
    double safety_score = 1.0 - clamp01(0.55 * herg_risk(herg_ic50_um) + 0.45 * cyp_risk(cyp_ic50_um));

    return clamp01(
        0.24 * potency +
        0.18 * selectivity +
        0.18 * lle_score +
        0.15 * solubility_score +
        0.15 * permeability_score +
        0.06 * safety_score +
        0.04 * qc
    );
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_medicinal_scoring_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_medicinal_scoring_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "compound_id,pIC50,LLE,selectivity_window,MPO_score\n");

    fprintf(fp, "MEDADV001,%.6f,%.6f,%.6f,%.6f\n",
        pic50_from_nm(18.0),
        lle(18.0, 3.2),
        selectivity_window(2100.0, 18.0),
        mpo_score(18.0, 2100.0, 3.2, 45.0, 18.0, 18.0, 22.0, 0.94)
    );

    fprintf(fp, "MEDADV008,%.6f,%.6f,%.6f,%.6f\n",
        pic50_from_nm(4.0),
        lle(4.0, 4.6),
        selectivity_window(4800.0, 4.0),
        mpo_score(4.0, 4800.0, 4.6, 34.0, 16.0, 25.0, 30.0, 0.91)
    );

    fclose(fp);
    printf("C medicinal scoring kernels complete.\n");
    return 0;
}
