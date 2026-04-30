/*
Soil Chemistry, Nutrient Cycles, and Land Systems
C++ soil-zone triage and land-system aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct SoilRecord {
    std::string site;
    std::string land_use;
    std::string soil_zone;
    double nutrient_balance;
    double leaching_pressure;
    double salinity_pressure;
    double ph_stress;
    double erosion_risk;
    double compaction_risk;
    double carbon_stability;
    double qc_score;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double soilPressure(const SoilRecord& r) {
    return clamp01(
        0.20 * (1.0 - r.nutrient_balance) +
        0.18 * r.leaching_pressure +
        0.16 * r.salinity_pressure +
        0.14 * r.ph_stress +
        0.12 * r.erosion_risk +
        0.10 * r.compaction_risk +
        0.07 * (1.0 - r.carbon_stability) +
        0.03 * (1.0 - r.qc_score)
    );
}

int main() {
    std::vector<SoilRecord> records = {
        {"Prairie-A", "cropland", "mollisol_like", 0.67, 0.16, 0.00, 0.00, 0.22, 0.18, 0.66, 0.94},
        {"Field-B", "intensive_cropland", "sandy_low_om", 0.56, 0.48, 0.00, 0.25, 0.46, 0.35, 0.28, 0.88},
        {"Irrigated-C", "irrigated_agriculture", "salinity_risk", 0.72, 0.34, 0.50, 0.20, 0.30, 0.25, 0.30, 0.86},
        {"Forest-D", "forest", "forest_soil", 0.34, 0.17, 0.00, 0.05, 0.12, 0.10, 0.82, 0.92},
        {"Degraded-E", "degraded_land", "eroded_low_om", 0.21, 0.66, 0.17, 0.45, 0.82, 0.65, 0.13, 0.78}
    };

    std::map<std::string, double> pressure_sum;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_soil_land_system_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_soil_land_system_triage.csv");
    }

    out << "site,land_use,soil_zone,soil_pressure,attention_flag\n";

    for (const auto& record : records) {
        double pressure = soilPressure(record);
        std::string flag = pressure >= 0.65 ? "high_attention" :
                           pressure >= 0.45 ? "moderate_attention" :
                           "monitor";

        out << record.site << ","
            << record.land_use << ","
            << record.soil_zone << ","
            << pressure << ","
            << flag << "\n";

        pressure_sum[record.land_use] += pressure;
        counts[record.land_use] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_soil_land_use_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_soil_land_use_summary.csv");
    }

    summary << "land_use,n,mean_soil_pressure\n";
    for (const auto& item : pressure_sum) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ soil land-system triage complete.\n";
    return 0;
}
