package main

import (
	"fmt"
)

const AvogadroConstant = 6.02214076e23

func NeutronNumber(massNumber int, atomicNumber int) int {
	return massNumber - atomicNumber
}

func IsotopeWeightedMass(masses []float64, abundances []float64) float64 {
	total := 0.0
	for i := range masses {
		total += masses[i] * abundances[i]
	}
	return total
}

func main() {
	chlorineMass := IsotopeWeightedMass(
		[]float64{34.96885268, 36.96590260},
		[]float64{0.7576, 0.2424},
	)

	fmt.Printf("chlorine_weighted_atomic_mass_u=%.6f\n", chlorineMass)
	fmt.Printf("carbon_14_neutron_number=%d\n", NeutronNumber(14, 6))
	fmt.Printf("one_mole_entities=%.6e\n", AvogadroConstant)
}
