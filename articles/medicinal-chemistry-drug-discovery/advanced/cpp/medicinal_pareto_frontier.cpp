/*
Medicinal Chemistry and Drug Discovery
C++ Pareto frontier and candidate triage model.
Synthetic educational code only.
*/

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct Candidate {
    std::string compound_id;
    double mpo;
    double selectivity_window;
    double lle;
    double safety_liability;
};

bool dominates(const Candidate& a, const Candidate& b) {
    bool better_or_equal =
        a.mpo >= b.mpo &&
        a.selectivity_window >= b.selectivity_window &&
        a.lle >= b.lle &&
        a.safety_liability <= b.safety_liability;

    bool strictly_better =
        a.mpo > b.mpo ||
        a.selectivity_window > b.selectivity_window ||
        a.lle > b.lle ||
        a.safety_liability < b.safety_liability;

    return better_or_equal && strictly_better;
}

int main() {
    std::vector<Candidate> candidates = {
        {"MEDADV001", 0.69, 116.7, 4.54, 0.10},
        {"MEDADV003", 0.63, 45.7, 5.35, 0.42},
        {"MEDADV006", 0.72, 162.5, 5.59, 0.00},
        {"MEDADV008", 0.76, 1200.0, 3.80, 0.08},
        {"MEDADV005", 0.38, 13.3, 1.72, 0.62}
    };

    std::vector<Candidate> frontier;

    for (const auto& candidate : candidates) {
        bool dominated = false;

        for (const auto& other : candidates) {
            if (candidate.compound_id == other.compound_id) {
                continue;
            }

            if (dominates(other, candidate)) {
                dominated = true;
                break;
            }
        }

        if (!dominated) {
            frontier.push_back(candidate);
        }
    }

    std::sort(frontier.begin(), frontier.end(), [](const Candidate& a, const Candidate& b) {
        return a.mpo > b.mpo;
    });

    std::ofstream out("../outputs/tables/cpp_medicinal_pareto_frontier.csv");
    if (!out) {
        out.open("outputs/tables/cpp_medicinal_pareto_frontier.csv");
    }

    out << "compound_id,MPO_score,selectivity_window,LLE,safety_liability\n";

    for (const auto& row : frontier) {
        out << row.compound_id << ","
            << row.mpo << ","
            << row.selectivity_window << ","
            << row.lle << ","
            << row.safety_liability << "\n";
    }

    std::cout << "C++ medicinal Pareto frontier complete.\n";
    return 0;
}
