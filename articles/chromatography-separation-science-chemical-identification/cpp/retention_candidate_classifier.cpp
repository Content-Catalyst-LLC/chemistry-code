#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct ReferenceCompound {
    std::string compound;
    double reference_retention_time_min;
};

int main() {
    std::vector<double> unknown_peak_times = {1.22, 2.85, 4.10, 5.36, 7.02};

    std::vector<ReferenceCompound> library = {
        {"solvent_front", 1.20},
        {"caffeine", 2.88},
        {"benzoic_acid", 4.06},
        {"acetophenone", 5.42},
        {"ethyl_vanillin", 7.00}
    };

    const double tolerance_min = 0.08;

    std::cout << "C++ retention-time candidate classifier\n";

    for (double peak_time : unknown_peak_times) {
        for (const auto& ref : library) {
            double delta = std::fabs(peak_time - ref.reference_retention_time_min);

            if (delta <= tolerance_min) {
                std::cout << "Peak at " << peak_time
                          << " min tentatively matches "
                          << ref.compound
                          << " with delta " << delta << " min\n";
            }
        }
    }

    std::cout << "Responsible-use note: retention-time matching alone is not definitive identification.\n";
    return 0;
}
