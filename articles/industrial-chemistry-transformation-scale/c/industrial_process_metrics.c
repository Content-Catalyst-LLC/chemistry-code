#include <stdio.h>

int main(void) {
    double theoreticalProduct = 1000.0;
    double actualProduct = 910.0;
    double waste = 210.0;
    double solvent = 350.0;
    double energy = 1600.0;
    double reactorVolume = 8.0;
    double timeH = 4.0;
    double volumetricFlow = 2.0;

    double yieldFraction = actualProduct / theoreticalProduct;
    double eFactor = waste / actualProduct;
    double solventIntensity = solvent / actualProduct;
    double energyIntensity = energy / actualProduct;
    double spaceTimeYield = actualProduct / (reactorVolume * timeH);
    double residenceTime = reactorVolume / volumetricFlow;

    printf("Industrial process metric utility\n");
    printf("Yield fraction: %.8f\n", yieldFraction);
    printf("E-factor: %.8f\n", eFactor);
    printf("Solvent intensity: %.8f\n", solventIntensity);
    printf("Energy intensity kWh/kg: %.8f\n", energyIntensity);
    printf("Space-time yield kg/m3/h: %.8f\n", spaceTimeYield);
    printf("Residence time h: %.8f\n", residenceTime);
    printf("Responsible-use note: synthetic educational calculation only.\n");

    return 0;
}
