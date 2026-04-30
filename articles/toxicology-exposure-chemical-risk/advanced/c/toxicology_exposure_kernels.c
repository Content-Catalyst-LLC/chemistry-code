/*
Toxicology, Exposure, and Chemical Risk
C exposure-dose and hazard quotient kernels.
Synthetic educational code only.
*/

#include <stdio.h>
#include <math.h>

double chronic_daily_intake(
    double concentration,
    double intake_rate,
    double exposure_frequency,
    double exposure_duration,
    double body_weight,
    double averaging_time
) {
    if (body_weight <= 0.0 || averaging_time <= 0.0) return 0.0;

    return concentration * intake_rate * exposure_frequency * exposure_duration /
           (body_weight * averaging_time);
}

double absorbed_dose(double cdi, double absorption_fraction) {
    return cdi * absorption_fraction;
}

double hazard_quotient(double dose, double reference_dose) {
    if (reference_dose <= 0.0) return 0.0;
    return dose / reference_dose;
}

double margin_of_exposure(double point_of_departure, double dose) {
    if (dose <= 0.0) return INFINITY;
    return point_of_departure / dose;
}

double cancer_risk_proxy(double dose, double slope_factor) {
    return dose * slope_factor;
}

int main(void) {
    FILE *fp = fopen("../outputs/tables/c_toxicology_exposure_kernels.csv", "w");
    if (!fp) {
        fp = fopen("outputs/tables/c_toxicology_exposure_kernels.csv", "w");
    }

    if (!fp) {
        fprintf(stderr, "Could not open output file.\n");
        return 1;
    }

    fprintf(fp, "record,cdi,absorbed_dose,hazard_quotient,margin_of_exposure,cancer_risk_proxy\n");

    double cdi = chronic_daily_intake(0.010, 2.0, 350.0, 30.0, 70.0, 10950.0);
    double dose = absorbed_dose(cdi, 0.95);

    fprintf(fp, "arsenic_water,%.10f,%.10f,%.6f,%.6f,%.10f\n",
        cdi,
        dose,
        hazard_quotient(dose, 0.0003),
        margin_of_exposure(0.008, dose),
        cancer_risk_proxy(dose, 1.5)
    );

    cdi = chronic_daily_intake(120.0, 0.0001, 180.0, 6.0, 15.0, 2190.0);
    dose = absorbed_dose(cdi, 0.40);

    fprintf(fp, "lead_soil_dust,%.10f,%.10f,%.6f,%.6f,%.10f\n",
        cdi,
        dose,
        hazard_quotient(dose, 0.0035),
        margin_of_exposure(0.05, dose),
        cancer_risk_proxy(dose, 0.0)
    );

    fclose(fp);
    printf("C toxicology exposure kernels complete.\n");
    return 0;
}
