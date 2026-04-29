#include <iomanip>
#include <iostream>

/*
Cation exchange capacity and base saturation example.

Base saturation percentage:
BS% = 100 * (Ca + Mg + K + Na) / CEC

All quantities must be in compatible charge-equivalent units.
*/

double base_saturation_percent(double base_cations, double cec) {
    return 100.0 * base_cations / cec;
}

const char* base_saturation_class(double bs) {
    if (bs < 40.0) return "low_base_saturation";
    if (bs < 70.0) return "moderate_base_saturation";
    return "high_base_saturation";
}

int main() {
    struct Case {
        const char* site;
        double cec;
        double base_cations;
    };

    Case cases[] = {
        {"Field-A", 12.0, 8.4},
        {"Field-B", 8.5, 4.2},
        {"Wetland-C", 36.0, 28.0},
        {"Mine-G", 7.0, 2.4}
    };

    std::cout << "site,cec_cmolc_kg,base_cations_cmolc_kg,base_saturation_percent,class\n";
    std::cout << std::fixed << std::setprecision(2);

    for (const auto& item : cases) {
        double bs = base_saturation_percent(item.base_cations, item.cec);
        std::cout << item.site << ","
                  << item.cec << ","
                  << item.base_cations << ","
                  << bs << ","
                  << base_saturation_class(bs) << "\n";
    }

    return 0;
}
