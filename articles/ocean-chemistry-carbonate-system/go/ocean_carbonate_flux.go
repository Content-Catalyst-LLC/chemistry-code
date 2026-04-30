package main

import (
	"fmt"
	"math"
)

func CarbonateAlpha2(pH float64) float64 {
	k1 := math.Pow(10.0, -6.0)
	k2 := math.Pow(10.0, -9.1)
	h := math.Pow(10.0, -pH)
	denominator := h*h + k1*h + k1*k2
	return k1 * k2 / denominator
}

func OmegaAragonite(calciumMmolKg float64, carbonateUmolKg float64) float64 {
	kspAragonite := 6.5e-7
	return (calciumMmolKg * 1.0e-3) * (carbonateUmolKg * 1.0e-6) / kspAragonite
}

func FluxProxy(pco2Water float64, pco2Air float64) float64 {
	return pco2Water - pco2Air
}

func main() {
	pH := 7.78
	dic := 2240.0
	calcium := 10.1
	pco2Water := 820.0

	alpha2 := CarbonateAlpha2(pH)
	carbonate := alpha2 * dic
	omega := OmegaAragonite(calcium, carbonate)
	flux := FluxProxy(pco2Water, 420.0)

	fmt.Println("Ocean carbonate chemistry example")
	fmt.Printf("pH: %.2f\n", pH)
	fmt.Printf("carbonate ion: %.2f umol/kg\n", carbonate)
	fmt.Printf("Omega aragonite: %.2f\n", omega)
	fmt.Printf("CO2 flux proxy: %.1f uatm\n", flux)
}
