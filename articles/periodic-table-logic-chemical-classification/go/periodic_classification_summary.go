package main

import (
	"fmt"
	"math"
)

func IsotopeWeightedMass(masses []float64, abundances []float64) float64 {
	total := 0.0
	for i := range masses {
		total += masses[i] * abundances[i]
	}
	return total
}

func NeutronNumber(massNumber int, atomicNumber int) int {
	return massNumber - atomicNumber
}

func FeatureDistance(a []float64, b []float64) float64 {
	sum := 0.0
	for i := range a {
		delta := a[i] - b[i]
		sum += delta * delta
	}
	return math.Sqrt(sum)
}

func main() {
	chlorineMass := IsotopeWeightedMass(
		[]float64{34.96885268, 36.96590260},
		[]float64{0.7576, 0.2424},
	)

	distance := FeatureDistance(
		[]float64{1.0, 2.0, 128.0, 520.0},
		[]float64{1.0, 3.0, 166.0, 496.0},
	)

	fmt.Printf("chlorine_weighted_atomic_mass_u=%.6f\n", chlorineMass)
	fmt.Printf("carbon_13_neutron_number=%d\n", NeutronNumber(13, 6))
	fmt.Printf("li_na_feature_distance_unscaled=%.6f\n", distance)
}
