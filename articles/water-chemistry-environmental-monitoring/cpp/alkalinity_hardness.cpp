#include <iomanip>
#include <iostream>

/*
Water chemistry calculation example.

Hardness as CaCO3 approximation:
hardness_mg_L_as_CaCO3 = 2.497 * Ca_mg_L + 4.118 * Mg_mg_L

Alkalinity is represented here as already measured in mg/L as CaCO3.
The example combines hardness and alkalinity into a simple interpretive table.
*/

double hardness_as_caco3(double calcium_mg_l, double magnesium_mg_l) {
    return 2.497 * calcium_mg_l + 4.118 * magnesium_mg_l;
}

const char* hardness_class(double hardness) {
    if (hardness < 60.0) return "soft";
    if (hardness < 120.0) return "moderately_hard";
    if (hardness < 180.0) return "hard";
    return "very_hard";
}

int main() {
    struct Case {
        const char* site;
        double calcium_mg_l;
        double magnesium_mg_l;
        double alkalinity_as_caco3_mg_l;
    };

    Case cases[] = {
        {"River-A", 62.0, 18.0, 145.0},
        {"Groundwater-C", 95.0, 34.0, 260.0},
        {"Mine-F", 18.0, 6.0, 22.0}
    };

    std::cout << "site,calcium_mg_L,magnesium_mg_L,hardness_as_CaCO3_mg_L,hardness_class,alkalinity_as_CaCO3_mg_L\n";
    std::cout << std::fixed << std::setprecision(2);

    for (const auto& item : cases) {
        double hardness = hardness_as_caco3(item.calcium_mg_l, item.magnesium_mg_l);
        std::cout << item.site << ","
                  << item.calcium_mg_l << ","
                  << item.magnesium_mg_l << ","
                  << hardness << ","
                  << hardness_class(hardness) << ","
                  << item.alkalinity_as_caco3_mg_l << "\n";
    }

    return 0;
}
