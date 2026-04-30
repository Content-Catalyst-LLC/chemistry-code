/*
Chemistry, Ethics, and the Governance of Molecular Power
C governance metric kernels.
Synthetic educational code only.
*/

#include <stdio.h>

double clamp01(double x) {
    if (x < 0.0) return 0.0;
    if (x > 1.0) return 1.0;
    return x;
}

double chemical_risk(double hazard, double exposure, double vulnerability, double persistence, double irreversibility) {
    double baseline = hazard * exposure * vulnerability;
    double durability = 0.5 * persistence + 0.5 * irreversibility;
    return clamp01(0.72 * baseline + 0.28 * durability);
}

double justice_weighted_risk(double risk, double inequality, double worker) {
    return clamp01(risk * (1.0 + 0.50 * inequality + 0.35 * worker));
}

double governance_gap(double justice_risk, double governance_strength) {
    return clamp01(justice_risk * (1.0 - governance_strength));
}

double stewardship_capacity(double stewardship, double governance, double monitoring, double alternatives) {
    return clamp01(0.35 * stewardship + 0.25 * governance + 0.20 * monitoring + 0.20 * alternatives);
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_molecular_power_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_molecular_power_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    double risk = chemical_risk(0.68, 0.76, 0.84, 0.62, 0.50);
    double jrisk = justice_weighted_risk(risk, 0.58, 0.72);

    fprintf(fp, "record,chemical_risk,justice_weighted_risk,governance_gap,stewardship_capacity\n");
    fprintf(fp, "high_volume_pesticide,%.8f,%.8f,%.8f,%.8f\n",
        risk,
        jrisk,
        governance_gap(jrisk, 0.55),
        stewardship_capacity(0.48, 0.55, 0.50, 0.62)
    );

    risk = chemical_risk(0.92, 0.35, 0.88, 0.60, 0.90);
    jrisk = justice_weighted_risk(risk, 0.52, 0.68);

    fprintf(fp, "restricted_toxic_precursor,%.8f,%.8f,%.8f,%.8f\n",
        risk,
        jrisk,
        governance_gap(jrisk, 0.88),
        stewardship_capacity(0.30, 0.88, 0.60, 0.80)
    );

    fclose(fp);
    printf("C molecular power kernels complete.\n");
    return 0;
}
