/*
Food Chemistry and the Molecular Basis of Nutrition
C++ food-matrix scenario model.
Synthetic educational code only.
*/

#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

struct FoodScenario {
    std::string food;
    double starch_g;
    double sugars_g;
    double fiber_g;
    double particle_accessibility;
    double processing_intensity;
};

double clamp01(double value) {
    return std::max(0.0, std::min(1.0, value));
}

double matrixProtection(double fiber_g, double particle_accessibility, double processing_intensity) {
    return clamp01(
        0.45 * clamp01(fiber_g / 12.0) +
        0.35 * (1.0 - particle_accessibility) +
        0.20 * (1.0 - processing_intensity)
    );
}

double glycemicAccessibility(const FoodScenario& food) {
    return clamp01(
        0.34 * clamp01(food.starch_g / 30.0) +
        0.26 * clamp01(food.sugars_g / 20.0) +
        0.22 * food.particle_accessibility +
        0.18 * food.processing_intensity -
        0.24 * matrixProtection(food.fiber_g, food.particle_accessibility, food.processing_intensity)
    );
}

int main() {
    std::vector<FoodScenario> foods = {
        {"oats_cooked", 18.0, 1.0, 8.0, 0.50, 0.30},
        {"white_bread", 24.0, 3.0, 1.0, 0.88, 0.75},
        {"lentils_cooked", 22.0, 3.0, 15.0, 0.45, 0.25}
    };

    std::ofstream out("../outputs/tables/cpp_food_matrix_scenarios.csv");
    if (!out) {
        out.open("outputs/tables/cpp_food_matrix_scenarios.csv");
    }

    out << "food,matrix_protection,glycemic_accessibility\n";

    for (const auto& food : foods) {
        double protection = matrixProtection(food.fiber_g, food.particle_accessibility, food.processing_intensity);
        double glycemic = glycemicAccessibility(food);
        out << food.food << "," << protection << "," << glycemic << "\n";
    }

    std::cout << "C++ food matrix scenarios complete.\n";
    return 0;
}
