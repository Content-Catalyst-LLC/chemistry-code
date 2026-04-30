package main

import (
	"fmt"
	"math"
)

func DesorptionRate(bindingEnergyK float64, dustTemperatureK float64) float64 {
	attemptFrequency := 1.0e12
	return attemptFrequency * math.Exp(-bindingEnergyK/dustTemperatureK)
}

func PhotodissociationLifetimeYears(uvIndex float64) float64 {
	baseRate := 1.0e-10
	secondsPerYear := 365.25 * 24.0 * 3600.0
	kph := baseRate * math.Max(uvIndex, 1.0e-12)
	return 1.0 / kph / secondsPerYear
}

func main() {
	fmt.Println("Astrochemical photochemistry and desorption example")

	cases := []struct {
		Species         string
		BindingEnergyK  float64
		DustTemperature float64
		UVIndex         float64
	}{
		{"CO", 855.0, 10.0, 0.2},
		{"CH3OH", 5500.0, 120.0, 8.0},
		{"H2O", 5700.0, 160.0, 12.0},
	}

	for _, item := range cases {
		kdes := DesorptionRate(item.BindingEnergyK, item.DustTemperature)
		lifetime := PhotodissociationLifetimeYears(item.UVIndex)
		fmt.Printf(
			"%s | k_des %.3e s^-1 | photodissociation lifetime %.3e years\n",
			item.Species,
			kdes,
			lifetime,
		)
	}
}
