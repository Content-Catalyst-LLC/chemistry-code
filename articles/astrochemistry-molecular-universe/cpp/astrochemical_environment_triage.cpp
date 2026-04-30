/*
Astrochemistry and the Molecular Universe
C++ astrochemical environment triage and molecular-family aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct AstroRecord {
    std::string region;
    std::string environment;
    std::string molecular_family;
    std::string species;
    double molecular_complexity;
    double ice_chemistry;
    double ionization_pressure;
    double freezeout_efficiency;
    double photodestruction_pressure;
    double qc_score;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double activityIndex(const AstroRecord& r) {
    double qc_penalty = 1.0 - r.qc_score;

    return clamp01(
        0.24 * r.molecular_complexity +
        0.22 * r.ice_chemistry +
        0.18 * r.ionization_pressure +
        0.16 * r.freezeout_efficiency +
        0.08 * qc_penalty -
        0.12 * r.photodestruction_pressure
    );
}

int main() {
    std::vector<AstroRecord> records = {
        {"Taurus_TMC1", "cold_dark_cloud", "carbon_chain", "HC3N", 0.55, 0.72, 0.28, 0.80, 0.01, 0.93},
        {"Orion_KL", "hot_core", "complex_organic", "CH3OCH3", 0.86, 0.48, 0.68, 0.72, 0.04, 0.90},
        {"TW_Hya", "disk_midplane", "ice_chemistry", "H2O_ice", 0.60, 0.92, 0.25, 0.95, 0.01, 0.91},
        {"Comet_67P", "cometary_coma", "volatile_ice", "CO", 0.44, 0.61, 0.24, 0.38, 0.20, 0.88},
        {"Titan", "planetary_atmosphere", "nitrile", "HCN", 0.70, 0.22, 0.55, 0.30, 0.35, 0.86}
    };

    std::map<std::string, double> sum_activity;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_astrochemical_environment_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_astrochemical_environment_triage.csv");
    }

    out << "region,environment,molecular_family,species,activity_index,attention_flag\n";

    for (const auto& record : records) {
        double activity = activityIndex(record);
        std::string flag = activity >= 0.65 ? "high_activity" :
                           activity >= 0.45 ? "moderate_activity" :
                           "low_to_monitor";

        out << record.region << ","
            << record.environment << ","
            << record.molecular_family << ","
            << record.species << ","
            << activity << ","
            << flag << "\n";

        sum_activity[record.environment] += activity;
        counts[record.environment] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_astrochemical_environment_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_astrochemical_environment_summary.csv");
    }

    summary << "environment,n,mean_activity_index\n";
    for (const auto& item : sum_activity) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ astrochemical environment triage complete.\n";
    return 0;
}
