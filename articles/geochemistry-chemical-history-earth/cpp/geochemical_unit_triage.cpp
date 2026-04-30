/*
Geochemistry and the Chemical History of Earth
C++ geologic unit triage and geochemical province aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Sample {
    std::string sample_id;
    std::string province;
    std::string rock_type;
    std::string tectonic_setting;
    double age_disagreement;
    double weathering_index;
    double mafic_index;
    double crustal_evolution_proxy;
    double redox_state_proxy;
    double qc_score;
};

double clamp01(double x) {
    return std::max(0.0, std::min(1.0, x));
}

double geochemicalPressure(const Sample& s) {
    double qc_penalty = 1.0 - s.qc_score;

    return clamp01(
        0.18 * s.age_disagreement +
        0.20 * s.weathering_index +
        0.16 * s.mafic_index +
        0.20 * s.crustal_evolution_proxy +
        0.20 * s.redox_state_proxy +
        0.06 * qc_penalty
    );
}

int main() {
    std::vector<Sample> samples = {
        {"GEOFS001", "Superior_Craton", "granite", "continental_crust", 0.84, 0.17, 0.04, 0.59, 0.25, 0.93},
        {"GEOFS002", "Mid_Ocean_Ridge", "basalt", "oceanic_crust", 20.15, 0.18, 0.27, 0.08, 0.52, 0.95},
        {"GEOFS005", "Himalayan_Foreland", "shale", "sedimentary_basin", 10.25, 0.42, 0.14, 0.78, 0.30, 0.89},
        {"GEOFS006", "Banded_Iron_Formation", "iron_formation", "precambrian_ocean", 0.42, 0.00, 0.54, 0.22, 0.92, 0.86},
        {"GEOFS008", "Siberian_Platform", "carbonate", "marine_sedimentary", 0.31, 0.00, 0.04, 0.26, 0.32, 0.91}
    };

    std::map<std::string, double> pressure_sum;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_geochemical_unit_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_geochemical_unit_triage.csv");
    }

    out << "sample_id,province,rock_type,tectonic_setting,geochemical_pressure,attention_flag\n";

    for (const auto& sample : samples) {
        double pressure = geochemicalPressure(sample);
        std::string flag = pressure >= 0.65 ? "high_attention" :
                           pressure >= 0.45 ? "moderate_attention" :
                           "monitor";

        out << sample.sample_id << ","
            << sample.province << ","
            << sample.rock_type << ","
            << sample.tectonic_setting << ","
            << pressure << ","
            << flag << "\n";

        pressure_sum[sample.tectonic_setting] += pressure;
        counts[sample.tectonic_setting] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_geochemical_tectonic_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_geochemical_tectonic_summary.csv");
    }

    summary << "tectonic_setting,n,mean_geochemical_pressure\n";
    for (const auto& item : pressure_sum) {
        summary << item.first << ","
                << counts[item.first] << ","
                << item.second / counts[item.first] << "\n";
    }

    std::cout << "C++ geochemical unit triage complete.\n";
    return 0;
}
