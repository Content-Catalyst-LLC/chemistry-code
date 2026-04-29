package main

import (
	"fmt"
	"math"
)

func BoltzmannWeight(deltaEKJMol float64, temperatureK float64) float64 {
	const R = 8.314462618
	return math.Exp(-(deltaEKJMol * 1000.0) / (R * temperatureK))
}

func LennardJones(distance float64, epsilon float64, sigma float64) float64 {
	ratio := sigma / distance
	return 4.0 * epsilon * (math.Pow(ratio, 12) - math.Pow(ratio, 6))
}

func Tanimoto(a float64, b float64, c float64) float64 {
	return c / (a + b - c)
}

func main() {
	fmt.Printf("boltzmann_weight=%.6f\n", BoltzmannWeight(2.5, 298.15))
	fmt.Printf("lennard_jones=%.6f\n", LennardJones(1.12, 1.0, 1.0))
	fmt.Printf("tanimoto=%.6f\n", Tanimoto(5.0, 4.0, 3.0))
}
