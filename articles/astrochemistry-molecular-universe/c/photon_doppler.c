#include <math.h>
#include <stdio.h>

/*
Astrochemical photon-energy and Doppler-shift example.

Educational only. Professional spectral analysis requires uncertainty,
rest-frequency catalogs, velocity frames, calibration, line blending,
and radiative-transfer context.
*/

double radial_velocity_km_s(double rest_frequency_ghz, double observed_frequency_ghz) {
    const double c_km_s = 299792.458;
    return -c_km_s * (observed_frequency_ghz - rest_frequency_ghz) / rest_frequency_ghz;
}

double photon_energy_j(double frequency_ghz) {
    const double h_j_s = 6.62607015e-34;
    return h_j_s * frequency_ghz * 1.0e9;
}

int main(void) {
    double rest[] = {115.271, 96.741, 88.632};
    double observed[] = {115.269, 96.738, 88.631};

    printf("case,rest_frequency_GHz,observed_frequency_GHz,radial_velocity_km_s,photon_energy_J\n");

    for (int i = 0; i < 3; i++) {
        printf(
            "%d,%.6f,%.6f,%.6f,%.8e\n",
            i + 1,
            rest[i],
            observed[i],
            radial_velocity_km_s(rest[i], observed[i]),
            photon_energy_j(rest[i])
        );
    }

    return 0;
}
