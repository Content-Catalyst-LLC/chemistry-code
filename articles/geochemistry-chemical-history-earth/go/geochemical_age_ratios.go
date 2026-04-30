package main

import (
	"fmt"
	"math"
)

func CIASimplified(al2o3 float64, cao float64, na2o float64, k2o float64) float64 {
	return 100.0 * al2o3 / (al2o3 + cao + na2o + k2o)
}

func Ratio(numerator float64, denominator float64) float64 {
	return numerator / denominator
}

func RadiometricAgeMa(parent float64, daughter float64, lambda float64) float64 {
	return (1.0 / lambda) * math.Log(1.0+daughter/parent) / 1.0e6
}

func IsotopeDelta(sampleRatio float64, standardRatio float64) float64 {
	return ((sampleRatio / standardRatio) - 1.0) * 1000.0
}

func main() {
	fmt.Println("Geochemical calculations")

	ciaBasalt := CIASimplified(15.4, 10.5, 2.9, 0.8)
	ciaSaprolite := CIASimplified(25.5, 0.8, 0.3, 1.2)
	rbSr := Ratio(165.0, 190.0)
	age := RadiometricAgeMa(1.0, 0.35, 1.55125e-10)
	deltaC := IsotopeDelta(0.01112, 0.01118)

	fmt.Printf("Basalt simplified CIA: %.2f\n", ciaBasalt)
	fmt.Printf("Weathered saprolite simplified CIA: %.2f\n", ciaSaprolite)
	fmt.Printf("Granite Rb/Sr: %.3f\n", rbSr)
	fmt.Printf("Simplified radiometric age: %.2f Ma\n", age)
	fmt.Printf("Delta carbon example: %.3f per mil\n", deltaC)
}
