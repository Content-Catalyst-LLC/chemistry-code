package main

import "fmt"

func ConcentrationFromCalibration(signal float64, slope float64, intercept float64) float64 {
	return (signal - intercept) / slope
}

func LOD(blankSD float64, slope float64) float64 {
	return 3.0 * blankSD / slope
}

func LOQ(blankSD float64, slope float64) float64 {
	return 10.0 * blankSD / slope
}

func ChromatographicResolution(tR1 float64, tR2 float64, w1 float64, w2 float64) float64 {
	return 2.0 * (tR2 - tR1) / (w1 + w2)
}

func BeerLambertConcentration(absorbance float64, epsilon float64, pathLength float64) float64 {
	return absorbance / (epsilon * pathLength)
}

func main() {
	fmt.Printf("unknown_concentration=%.6f\n", ConcentrationFromCalibration(3.72, 0.515, 0.04))
	fmt.Printf("LOD=%.6f\n", LOD(0.0032, 0.515))
	fmt.Printf("LOQ=%.6f\n", LOQ(0.0032, 0.515))
	fmt.Printf("resolution=%.6f\n", ChromatographicResolution(3.10, 5.20, 0.42, 0.50))
	fmt.Printf("beer_lambert_c=%.8f\n", BeerLambertConcentration(0.625, 12500.0, 1.0))
}
