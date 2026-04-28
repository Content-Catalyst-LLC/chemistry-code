package main

import (
	"fmt"
	"math"
)

func LimitingExtent(available []float64, coefficients []float64) float64 {
	minimum := math.Inf(1)
	for i := range available {
		extent := available[i] / coefficients[i]
		if extent < minimum {
			minimum = extent
		}
	}
	return minimum
}

func PercentYield(actual float64, theoretical float64) float64 {
	return actual / theoretical * 100.0
}

func DilutionVolume(c1 float64, c2 float64, v2 float64) float64 {
	return (c2 * v2) / c1
}

func main() {
	extent := LimitingExtent([]float64{4.0, 1.5}, []float64{2.0, 1.0})
	waterMol := extent * 2.0
	theoreticalYield := waterMol * 18.01528

	fmt.Printf("maximum_extent_mol=%.6f\n", extent)
	fmt.Printf("water_mol_theoretical=%.6f\n", waterMol)
	fmt.Printf("theoretical_yield_g=%.6f\n", theoreticalYield)
	fmt.Printf("percent_yield=%.6f\n", PercentYield(45.0, theoreticalYield))
	fmt.Printf("stock_volume_L=%.6f\n", DilutionVolume(1.0, 0.1, 0.25))
}
