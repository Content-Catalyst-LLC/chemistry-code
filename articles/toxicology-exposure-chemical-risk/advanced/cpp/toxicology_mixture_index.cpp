/*
Toxicology, Exposure, and Chemical Risk
C++ mixture hazard-index and target-system aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct ExposureRecord {
    std::string chemical;
    std::string target_system;
    std::string mixture_group;
    double hazard_quotient;
    double vulnerability_factor;
};

int main() {
    std::vector<ExposureRecord> records = {
        {"arsenic", "cancer_and_skin", "metals_metalloids", 0.030, 1.20},
        {"lead", "neurodevelopment", "metals_metalloids", 0.120, 1.80},
        {"mercury", "neurodevelopment", "metals_metalloids", 0.420, 1.50},
        {"chlorpyrifos", "neurodevelopment", "pesticides", 0.210, 1.70},
        {"ozone", "respiratory", "air_pollutants", 0.190, 1.25},
        {"formaldehyde", "respiratory", "irritants", 0.085, 1.05}
    };

    std::map<std::string, double> target_hazard_index;
    std::map<std::string, double> target_vulnerability_index;
    std::map<std::string, double> mixture_hazard_index;

    for (const auto& record : records) {
        target_hazard_index[record.target_system] += record.hazard_quotient;
        target_vulnerability_index[record.target_system] += record.hazard_quotient * record.vulnerability_factor;
        mixture_hazard_index[record.mixture_group] += record.hazard_quotient;
    }

    std::ofstream out("../outputs/tables/cpp_toxicology_mixture_index.csv");
    if (!out) {
        out.open("outputs/tables/cpp_toxicology_mixture_index.csv");
    }

    out << "summary_type,group,hazard_index,vulnerability_adjusted_hazard_index\n";

    for (const auto& item : target_hazard_index) {
        out << "target_system,"
            << item.first << ","
            << item.second << ","
            << target_vulnerability_index[item.first] << "\n";
    }

    for (const auto& item : mixture_hazard_index) {
        out << "mixture_group,"
            << item.first << ","
            << item.second << ","
            << item.second << "\n";
    }

    std::cout << "C++ toxicology mixture index complete.\n";
    return 0;
}
