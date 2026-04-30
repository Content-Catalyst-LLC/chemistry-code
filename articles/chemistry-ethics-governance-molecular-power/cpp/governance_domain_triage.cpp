/*
Chemistry, Ethics, and the Governance of Molecular Power
C++ governance-domain triage and aggregation.
Synthetic educational code only.
*/

#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

struct Record {
    std::string domain;
    std::string context;
    double benefit;
    double justice_risk;
    double governance_gap;
    double responsible_score;
    double dual_use;
};

int main() {
    std::vector<Record> records = {
        {"medicine", "essential_therapeutic", 0.95, 0.18, 0.03, 0.72, 0.05},
        {"agriculture", "high_volume_pesticide", 0.72, 0.58, 0.26, 0.43, 0.12},
        {"industrial_material", "persistent_additive", 0.58, 0.67, 0.39, 0.31, 0.08},
        {"consumer_product", "indoor_exposure_chemical", 0.48, 0.55, 0.34, 0.28, 0.04},
        {"dual_use", "restricted_toxic_precursor", 0.22, 0.62, 0.07, 0.20, 0.95}
    };

    std::map<std::string, double> gap_sum;
    std::map<std::string, double> score_sum;
    std::map<std::string, int> counts;

    std::ofstream out("../outputs/tables/cpp_governance_domain_triage.csv");
    if (!out) {
        out.open("outputs/tables/cpp_governance_domain_triage.csv");
    }

    out << "domain,context,governance_gap,responsible_score,governance_flag\n";

    for (const auto& r : records) {
        std::string flag = r.dual_use >= 0.80 ? "restricted_or_high_dual_use_governance_attention" :
                           r.governance_gap >= 0.35 ? "high_governance_gap" :
                           r.justice_risk >= 0.55 ? "high_justice_weighted_risk" :
                           "monitor_and_improve_governance";

        out << r.domain << ","
            << r.context << ","
            << r.governance_gap << ","
            << r.responsible_score << ","
            << flag << "\n";

        gap_sum[r.domain] += r.governance_gap;
        score_sum[r.domain] += r.responsible_score;
        counts[r.domain] += 1;
    }

    std::ofstream summary("../outputs/tables/cpp_governance_domain_summary.csv");
    if (!summary) {
        summary.open("outputs/tables/cpp_governance_domain_summary.csv");
    }

    summary << "domain,n,mean_governance_gap,mean_responsible_score\n";
    for (const auto& item : counts) {
        summary << item.first << ","
                << item.second << ","
                << gap_sum[item.first] / item.second << ","
                << score_sum[item.first] / item.second << "\n";
    }

    std::cout << "C++ governance domain triage complete.\n";
    return 0;
}
