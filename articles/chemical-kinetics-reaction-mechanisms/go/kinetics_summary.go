package main

import (
	"fmt"
	"math"
)

const R = 8.314462618

func FirstOrderConcentration(c0 float64, k float64, t float64) float64 {
	return c0 * math.Exp(-k*t)
}

func HalfLifeFirstOrder(k float64) float64 {
	return math.Log(2.0) / k
}

func ArrheniusRateConstant(a float64, eaJMol float64, temperatureK float64) float64 {
	return a * math.Exp(-eaJMol/(R*temperatureK))
}

func main() {
	fmt.Printf("first_order_concentration_t20=%.6f\n", FirstOrderConcentration(1.0, 0.15, 20.0))
	fmt.Printf("first_order_half_life=%.6f\n", HalfLifeFirstOrder(0.15))
	fmt.Printf("arrhenius_k_310K=%.6f\n", ArrheniusRateConstant(1.0e7, 55000.0, 310.0))
}
