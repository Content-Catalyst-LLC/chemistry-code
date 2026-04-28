package main

import (
	"fmt"
	"math"
)

const R = 8.314462618
const F = 96485.33212

func CellPotential(eCathode float64, eAnode float64) float64 {
	return eCathode - eAnode
}

func DeltaG(n float64, eCell float64) float64 {
	return -n * F * eCell / 1000.0
}

func Nernst(e0 float64, n float64, q float64, temperatureK float64) float64 {
	return e0 - (R*temperatureK/(n*F))*math.Log(q)
}

func main() {
	eCell := CellPotential(0.34, -0.76)
	dg := DeltaG(2.0, eCell)
	eNonstandard := Nernst(1.10, 2.0, 100.0, 298.15)

	fmt.Printf("E_cell_standard_V=%.6f\n", eCell)
	fmt.Printf("delta_g_standard_kj_mol=%.6f\n", dg)
	fmt.Printf("E_nonstandard_V=%.6f\n", eNonstandard)
}
