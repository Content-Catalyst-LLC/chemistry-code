/*
Water Chemistry and Environmental Monitoring
C++ water-body summary and monitoring triage.
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
    std::string site;
    std::string water_body;
    std::string analyte;
    double benchmark_ratio;
    double oxygen_stress;
    double nutrient_index;
    double metal_index;
    double turbidity_pressure;
    double qc_score;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double pressureIndex(const Record& r) {
    double ratio_component = clamp01(std::log1p(r.benchmark_ratio) / std::log(4.0));
    double qc_penalty = 1.0 - r.qc_score;

    return clamp01(
        0.22 * ratio_component +
        0.18 * r.oxygen_stress +
        0.20 * r.nutrient_index +
        0.20 * r.metal_index +
        0.12 * r.turbidity_pressure +
        0.08 * qc_penalty
    );
}

int main() {
    std::vector<Record> records = {
        {"River-A", "river", "nitrate_as_N", 0.78, 0.13, 0.84, 0.25, 0.12, 0.93},
        {"Lake-B", "lake", "dissolved_oxygen", 0.92, 0.54, 0.39, 0.18, 0.18, 0.88},
        {"Well-C", "aquifer", "arsenic", 1.20, 0.75, 0.06, 0.44, 0.01, 0.86},
        {"Storm-D", "urban_runoff", "lead", 1.20, 0.30, 1.00, 0.88, 0.75, 0.80},
        {"Estuary-E", "estuary", "copper", 1.08, 0.25, 0.87, 0.55, 0.22, 0.84}
    };

    std::map<std::string, double> pressure_sum;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_water_body_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_water_body_triage.csv");
    }

    out << "site,water_body,analyte,pressure_index,attention_flag\n";

    for (const auto& record : records) {
        double pressure = pressureIndex(record);
        std::string flag = pressure >= 0.65 ? "high_attention" :
                           pressure >= 0.45 ? "moderate_attention" :
                           "monitor";

        out << record.site << ","
            << record.water_body << ","
            << record.analyte << ","
            << pressure << ","
            << flag << "\n";

        pressure_sum[record.water_body] += pressure;
        counts[record.water_body] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_water_body_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_water_body_summary.csv");
    }

    summary << "water_body,n,mean_pressure_index\n";
    for (const auto& item : pressure_sum) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ water-body triage complete.\n";
    return 0;
}
