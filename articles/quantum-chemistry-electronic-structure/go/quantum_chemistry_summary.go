package main

import (
	"fmt"
	"math"
)

func BoltzmannWeight(deltaEKJMol float64, temperatureK float64) float64 {
	const R = 8.314462618
	return math.Exp(-(deltaEKJMol * 1000.0) / (R * temperatureK))
}

func TSTRate(deltaGDaggerKJMol float64, temperatureK float64) float64 {
	const kB = 1.380649e-23
	const h = 6.62607015e-34
	const R = 8.314462618
	return (kB * temperatureK / h) * math.Exp(-(deltaGDaggerKJMol*1000.0)/(R*temperatureK))
}

func TwoLevelEnergies(ea float64, eb float64, v float64) (float64, float64) {
	trace := ea + eb
	diff := ea - eb
	split := math.Sqrt(diff*diff + 4.0*v*v)
	return (trace - split) / 2.0, (trace + split) / 2.0
}

func main() {
	e1, e2 := TwoLevelEnergies(-10.0, -8.0, -2.0)
	fmt.Printf("two_level_E1=%.6f\n", e1)
	fmt.Printf("two_level_E2=%.6f\n", e2)
	fmt.Printf("boltzmann_weight=%.10f\n", BoltzmannWeight(25.0, 298.15))
	fmt.Printf("tst_rate=%.6e\n", TSTRate(50.0, 298.15))
}
