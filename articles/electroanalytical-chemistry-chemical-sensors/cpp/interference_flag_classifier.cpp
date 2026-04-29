#include <cmath>
#include <iostream>
#include <string>
#include <vector>

struct InterferenceTest {
    std::string interferent;
    double response_change_percent;
};

int main() {
    std::vector<InterferenceTest> tests = {
        {"ascorbate", 3.6},
        {"uric_acid", 4.8},
        {"acetaminophen", 8.4},
        {"chloride", 0.5},
        {"none", 0.0}
    };

    const double flag_threshold_percent = 5.0;

    std::cout << "C++ electrochemical interference flag classifier\n";

    for (const auto& test : tests) {
        if (std::fabs(test.response_change_percent) >= flag_threshold_percent) {
            std::cout << test.interferent
                      << " flagged with response change "
                      << test.response_change_percent
                      << "%\n";
        }
    }

    std::cout << "Responsible-use note: synthetic educational interference screening only.\n";
    return 0;
}
