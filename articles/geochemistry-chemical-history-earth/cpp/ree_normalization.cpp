#include <iomanip>
#include <iostream>
#include <map>
#include <string>

/*
Simplified rare-earth-element normalization example.

This uses a small synthetic reference set for teaching only.
Professional workflows require appropriate reference reservoirs,
analytical uncertainty, detection limits, and petrologic context.
*/

int main() {
    std::map<std::string, double> sample = {
        {"La", 32.0},
        {"Ce", 68.0},
        {"Nd", 28.0}
    };

    std::map<std::string, double> reference = {
        {"La", 0.237},
        {"Ce", 0.613},
        {"Nd", 0.457}
    };

    std::cout << "element,sample_ppm,reference_ppm,normalized_value\n";
    std::cout << std::fixed << std::setprecision(4);

    for (const auto& item : sample) {
        const std::string& element = item.first;
        double normalized = item.second / reference[element];

        std::cout << element << ","
                  << item.second << ","
                  << reference[element] << ","
                  << normalized << "\n";
    }

    return 0;
}
