/*
Atmospheric Chemistry and Climate Processes
C++ atmospheric class triage and aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Record {
    std::string station;
    std::string chemical_class;
    std::string species;
    double reference_ratio;
    double forcing_component;
    double ozone_component;
    double aerosol_component;
    double persistence_component;
    double qc_score;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double pressureIndex(const Record& r) {
    double qc_penalty = 1.0 - r.qc_score;

    if (r.chemical_class == "greenhouse_gas") {
        return clamp01(
            0.24 * r.reference_ratio +
            0.36 * r.forcing_component +
            0.25 * r.persistence_component +
            0.10 * r.ozone_component +
            0.05 * qc_penalty
        );
    }

    if (r.chemical_class == "aerosol") {
        return clamp01(
            0.24 * r.reference_ratio +
            0.34 * r.aerosol_component +
            0.18 * r.persistence_component +
            0.14 * r.ozone_component +
            0.10 * qc_penalty
        );
    }

    return clamp01(
        0.25 * r.reference_ratio +
        0.35 * r.ozone_component +
        0.15 * r.aerosol_component +
        0.15 * r.persistence_component +
        0.10 * qc_penalty
    );
}

int main() {
    std::vector<Record> records = {
        {"Global-CO2", "greenhouse_gas", "CO2", 0.72, 0.58, 0.00, 0.05, 0.99, 0.95},
        {"Global-CH4", "greenhouse_gas", "CH4", 0.95, 0.31, 0.00, 0.04, 0.99, 0.94},
        {"Urban-O3", "secondary_pollutant", "O3", 0.54, 0.00, 0.65, 0.09, 0.01, 0.90},
        {"Wildfire-PM", "aerosol", "PM2.5", 0.92, 0.00, 0.34, 0.75, 0.14, 0.84},
        {"Dust-AOD", "aerosol", "coarse_aerosol", 0.88, 0.00, 0.05, 0.84, 0.19, 0.82}
    };

    std::map<std::string, double> sum_pressure;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_atmospheric_class_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_atmospheric_class_triage.csv");
    }

    out << "station,chemical_class,species,pressure_index,attention_flag\n";

    for (const auto& record : records) {
        double pressure = pressureIndex(record);
        std::string flag = pressure >= 0.65 ? "high_attention" :
                           pressure >= 0.45 ? "moderate_attention" :
                           "monitor";

        out << record.station << ","
            << record.chemical_class << ","
            << record.species << ","
            << pressure << ","
            << flag << "\n";

        sum_pressure[record.chemical_class] += pressure;
        counts[record.chemical_class] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_atmospheric_class_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_atmospheric_class_summary.csv");
    }

    summary << "chemical_class,n,mean_pressure_index\n";
    for (const auto& item : sum_pressure) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ atmospheric class triage complete.\n";
    return 0;
}
