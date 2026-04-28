package main

import (
	"fmt"
	"math"
)

func WeakAcidHydronium(ka float64, concentration float64) float64 {
	return (-ka + math.Sqrt(math.Pow(ka, 2)+4.0*ka*concentration)) / 2.0
}

func PHFromHydronium(h float64) float64 {
	return -math.Log10(h)
}

func HendersonHasselbalch(pka float64, base float64, acid float64) float64 {
	return pka + math.Log10(base/acid)
}

func main() {
	h := WeakAcidHydronium(1.8e-5, 0.100)
	ph := PHFromHydronium(h)
	bufferPH := HendersonHasselbalch(4.76, 0.120, 0.100)

	fmt.Printf("weak_acid_hydronium=%.8f\n", h)
	fmt.Printf("weak_acid_pH=%.6f\n", ph)
	fmt.Printf("buffer_pH=%.6f\n", bufferPH)
}
