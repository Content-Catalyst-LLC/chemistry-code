package main

import (
	"fmt"
	"math"
)

const R = 8.314462618

func RateEnhancement(deltaEaKJMol float64, temperatureK float64) float64 {
	return math.Exp((deltaEaKJMol * 1000.0) / (R * temperatureK))
}

func TurnoverNumber(productMol float64, catalystMol float64) float64 {
	return productMol / catalystMol
}

func TurnoverFrequency(productMol float64, catalystMol float64, timeS float64) float64 {
	return TurnoverNumber(productMol, catalystMol) / timeS
}

func LangmuirTheta(k float64, p float64) float64 {
	return (k * p) / (1.0 + k*p)
}

func main() {
	fmt.Printf("rate_enhancement=%.6f\n", RateEnhancement(25.0, 298.15))
	fmt.Printf("TON=%.6f\n", TurnoverNumber(0.05, 0.0005))
	fmt.Printf("TOF=%.8f\n", TurnoverFrequency(0.05, 0.0005, 3600.0))
	fmt.Printf("theta=%.6f\n", LangmuirTheta(1.5, 1.0))
}
