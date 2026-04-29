package main

import (
	"fmt"
	"math"
)

const R = 8.314462618
const F = 96485.33212

func EquilibriumConstant(deltaGKJMol float64, temperatureK float64) float64 {
	return math.Exp(-(deltaGKJMol * 1000.0) / (R * temperatureK))
}

func Arrhenius(a float64, eaKJMol float64, temperatureK float64) float64 {
	return a * math.Exp(-(eaKJMol * 1000.0) / (R * temperatureK))
}

func Nernst(e0 float64, n float64, q float64, temperatureK float64) float64 {
	return e0 - (R*temperatureK/(n*F))*math.Log(q)
}

func main() {
	fmt.Printf("K_demo=%.6f\n", EquilibriumConstant(-20.0, 298.15))
	fmt.Printf("k_demo=%.6e\n", Arrhenius(1.0e12, 75.0, 298.15))
	fmt.Printf("E_demo=%.6f\n", Nernst(1.10, 2.0, 100.0, 298.15))
}
