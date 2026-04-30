#include <iomanip>
#include <iostream>

/*
Simplified Revelle-factor intuition.

R = (delta pCO2 / pCO2) / (delta DIC / DIC)

This is a conceptual teaching calculation, not a full carbonate-system model.
*/

double revelle_factor(double pco2_initial, double pco2_final, double dic_initial, double dic_final) {
    double relative_pco2_change = (pco2_final - pco2_initial) / pco2_initial;
    double relative_dic_change = (dic_final - dic_initial) / dic_initial;
    return relative_pco2_change / relative_dic_change;
}

int main() {
    double pco2_initial = 410.0;
    double pco2_final = 455.0;
    double dic_initial = 2050.0;
    double dic_final = 2080.0;

    double revelle = revelle_factor(pco2_initial, pco2_final, dic_initial, dic_final);

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Simplified Revelle-factor example\n";
    std::cout << "Initial pCO2: " << pco2_initial << " uatm\n";
    std::cout << "Final pCO2: " << pco2_final << " uatm\n";
    std::cout << "Initial DIC: " << dic_initial << " umol/kg\n";
    std::cout << "Final DIC: " << dic_final << " umol/kg\n";
    std::cout << "Revelle factor: " << revelle << "\n";

    return 0;
}
