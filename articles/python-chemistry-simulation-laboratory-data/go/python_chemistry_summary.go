package main

import (
	"fmt"
	"math"
)

func UnknownConcentration(response float64, slope float64, intercept float64) float64 {
	return (response - intercept) / slope
}

func FirstOrderConcentration(c0 float64, k float64, t float64) float64 {
	return c0 * math.Exp(-k*t)
}

func HalfLifeFirstOrder(k float64) float64 {
	return math.Log(2.0) / k
}

func StandardError(sd float64, n float64) float64 {
	return sd / math.Sqrt(n)
}

func main() {
	fmt.Printf("unknown_concentration_mM=%.6f\n", UnknownConcentration(0.95, 0.30, 0.02))
	fmt.Printf("first_order_concentration_mM=%.6f\n", FirstOrderConcentration(10.0, 0.015, 100.0))
	fmt.Printf("half_life_s=%.6f\n", HalfLifeFirstOrder(0.015))
	fmt.Printf("standard_error=%.6f\n", StandardError(0.03, 3.0))
}
