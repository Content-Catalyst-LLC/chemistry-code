/*
Ocean Chemistry and the Carbonate System
C++ ocean-region triage and carbonate-system aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct OceanRecord {
    std::string region;
    std::string water_mass;
    double acidification_pressure;
    double deoxygenation_pressure;
    double nutrient_upwelling_index;
    double buffer_proxy;
    double omega_aragonite;
    double qc_score;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double carbonatePressure(const OceanRecord& r) {
    double saturation_stress = clamp01((3.0 - r.omega_aragonite) / 3.0);
    double qc_penalty = 1.0 - r.qc_score;

    return clamp01(
        0.36 * r.acidification_pressure +
        0.20 * r.deoxygenation_pressure +
        0.16 * r.nutrient_upwelling_index +
        0.14 * (1.0 - r.buffer_proxy) +
        0.09 * saturation_stress +
        0.05 * qc_penalty
    );
}

int main() {
    std::vector<OceanRecord> records = {
        {"North_Atlantic", "surface_subpolar", 0.18, 0.00, 0.16, 0.92, 3.17, 0.94},
        {"Equatorial_Pacific", "surface_upwelling", 0.34, 0.00, 0.46, 0.70, 2.47, 0.91},
        {"North_Pacific", "intermediate_water", 0.65, 0.39, 0.80, 0.42, 1.43, 0.88},
        {"Arabian_Sea", "oxygen_minimum_zone", 0.88, 0.90, 0.91, 0.28, 1.05, 0.84},
        {"Caribbean_Reef", "surface_tropical", 0.08, 0.00, 0.02, 0.98, 3.68, 0.93}
    };

    std::map<std::string, double> sum_pressure;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_ocean_region_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_ocean_region_triage.csv");
    }

    out << "region,water_mass,carbonate_pressure,attention_flag\n";

    for (const auto& record : records) {
        double pressure = carbonatePressure(record);
        std::string flag = pressure >= 0.65 ? "high_attention" :
                           pressure >= 0.45 ? "moderate_attention" :
                           "monitor";

        out << record.region << ","
            << record.water_mass << ","
            << pressure << ","
            << flag << "\n";

        sum_pressure[record.water_mass] += pressure;
        counts[record.water_mass] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_ocean_water_mass_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_ocean_water_mass_summary.csv");
    }

    summary << "water_mass,n,mean_carbonate_pressure\n";
    for (const auto& item : sum_pressure) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ ocean region triage complete.\n";
    return 0;
}
