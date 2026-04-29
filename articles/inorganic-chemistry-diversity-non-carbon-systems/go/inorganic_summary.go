package main

import (
	"fmt"
	"math"
)

func OxidationState(totalCharge float64, knownContribution float64, unknownAtomCount float64) float64 {
	return (totalCharge - knownContribution) / unknownAtomCount
}

func CFSE(t2gElectrons float64, egElectrons float64, deltaO float64) float64 {
	return t2gElectrons*(-0.4*deltaO) + egElectrons*(0.6*deltaO)
}

func SpinOnlyMoment(unpairedElectrons float64) float64 {
	return math.Sqrt(unpairedElectrons * (unpairedElectrons + 2.0))
}

func ToleranceFactor(rA float64, rB float64, rX float64) float64 {
	return (rA + rX) / (math.Sqrt(2.0) * (rB + rX))
}

func main() {
	fmt.Printf("Mn_in_KMnO4_OS=%.6f\n", OxidationState(0.0, -7.0, 1.0))
	fmt.Printf("octahedral_d3_CFSE=%.6f\n", CFSE(3.0, 0.0, 1.0))
	fmt.Printf("spin_only_d3=%.6f\n", SpinOnlyMoment(3.0))
	fmt.Printf("tolerance_factor=%.6f\n", ToleranceFactor(1.60, 0.60, 1.40))
}
