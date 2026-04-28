package main

import (
	"fmt"
	"math"
)

const R = 8.314462618

func GibbsFreeEnergy(deltaHKJMol float64, deltaSJMolK float64, temperatureK float64) float64 {
	return deltaHKJMol - temperatureK*deltaSJMolK/1000.0
}

func EquilibriumConstant(deltaGStandardKJMol float64, temperatureK float64) float64 {
	return math.Exp(-(deltaGStandardKJMol * 1000.0) / (R * temperatureK))
}

func CalorimetryDeltaH(massG float64, specificHeatJGK float64, deltaTK float64, amountMol float64) float64 {
	qSolutionJ := massG * specificHeatJGK * deltaTK
	qReactionJ := -qSolutionJ
	return qReactionJ / 1000.0 / amountMol
}

func main() {
	dg := GibbsFreeEnergy(-80.0, -100.0, 298.15)
	k := EquilibriumConstant(dg, 298.15)
	dhCal := CalorimetryDeltaH(100.0, 4.184, 6.2, 0.0500)

	fmt.Printf("delta_g_kj_mol=%.6f\n", dg)
	fmt.Printf("equilibrium_constant=%.6f\n", k)
	fmt.Printf("calorimetry_delta_h_kj_mol=%.6f\n", dhCal)
}
