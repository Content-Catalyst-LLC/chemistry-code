#include <iomanip>
#include <iostream>

double concentration_from_calibration(double signal, double slope, double intercept) {
    return (signal - intercept) / slope;
}

double lod(double blank_sd, double slope) {
    return 3.0 * blank_sd / slope;
}

double loq(double blank_sd, double slope) {
    return 10.0 * blank_sd / slope;
}

double chromatographic_resolution(double tr1, double tr2, double w1, double w2) {
    return 2.0 * (tr2 - tr1) / (w1 + w2);
}

double beer_lambert_concentration(double absorbance, double epsilon, double path_length) {
    return absorbance / (epsilon * path_length);
}

int main() {
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "unknown_concentration=" << concentration_from_calibration(3.72, 0.515, 0.04) << "\n";
    std::cout << "LOD=" << lod(0.0032, 0.515) << "\n";
    std::cout << "LOQ=" << loq(0.0032, 0.515) << "\n";
    std::cout << "resolution=" << chromatographic_resolution(3.10, 5.20, 0.42, 0.50) << "\n";
    std::cout << std::setprecision(8);
    std::cout << "beer_lambert_c=" << beer_lambert_concentration(0.625, 12500.0, 1.0) << "\n";
    return 0;
}
