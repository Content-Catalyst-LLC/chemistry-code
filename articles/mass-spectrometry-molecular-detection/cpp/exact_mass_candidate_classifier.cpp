#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct Feature {
    std::string feature_id;
    double observed_mz;
    int charge;
};

struct Candidate {
    std::string name;
    double theoretical_mz;
    int expected_charge;
};

int main() {
    std::vector<Feature> features = {
        {"f1", 195.0878, 1},
        {"f2", 301.1412, 1},
        {"f3", 451.2129, 2},
        {"f4", 663.4521, 3}
    };

    std::vector<Candidate> candidates = {
        {"caffeine_candidate", 195.08765, 1},
        {"flavonoid_candidate", 301.14105, 1},
        {"peptide_candidate", 451.21340, 2},
        {"lipid_candidate", 663.45180, 3}
    };

    const double ppm_tolerance = 5.0;

    std::cout << "C++ exact-mass candidate classifier\n";

    for (const auto& feature : features) {
        for (const auto& candidate : candidates) {
            if (feature.charge != candidate.expected_charge) {
                continue;
            }

            double ppm_error = (feature.observed_mz - candidate.theoretical_mz)
                / candidate.theoretical_mz * 1000000.0;

            if (std::fabs(ppm_error) <= ppm_tolerance) {
                std::cout << feature.feature_id
                          << " tentatively matches "
                          << candidate.name
                          << " with ppm error "
                          << ppm_error
                          << "\n";
            }
        }
    }

    std::cout << "Responsible-use note: exact mass alone is not definitive identification.\n";
    return 0;
}
