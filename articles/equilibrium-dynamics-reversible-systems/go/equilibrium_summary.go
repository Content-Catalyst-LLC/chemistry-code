package main

import (
	"fmt"
	"math"
)

const R = 8.314462618

func DeltaGFromQK(q float64, k float64, temperatureK float64) float64 {
	return R * temperatureK * math.Log(q/k) / 1000.0
}

func SolveIsomerization(k float64, total float64) (float64, float64) {
	aEq := total / (1.0 + k)
	bEq := total - aEq
	return aEq, bEq
}

func ReversibleStep(a float64, b float64, kf float64, kr float64, dt float64) (float64, float64) {
	net := kf*a - kr*b
	aNext := math.Max(a-net*dt, 0.0)
	bNext := math.Max(b+net*dt, 0.0)
	return aNext, bNext
}

func main() {
	aEq, bEq := SolveIsomerization(4.0, 1.0)
	dg := DeltaGFromQK(0.5, 4.0, 298.15)
	a1, b1 := ReversibleStep(1.0, 0.0, 0.20, 0.05, 0.25)

	fmt.Printf("A_eq=%.6f\n", aEq)
	fmt.Printf("B_eq=%.6f\n", bEq)
	fmt.Printf("delta_g_kj_mol=%.6f\n", dg)
	fmt.Printf("A_after_step=%.6f\n", a1)
	fmt.Printf("B_after_step=%.6f\n", b1)
}
