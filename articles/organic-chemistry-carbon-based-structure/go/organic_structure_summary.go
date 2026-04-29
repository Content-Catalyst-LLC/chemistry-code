package main

import "fmt"

func DBE(c float64, h float64, n float64, x float64) float64 {
	return c - (h+x)/2.0 + n/2.0 + 1.0
}

func PolarityScore(heteroatoms float64, donors float64, acceptors float64) float64 {
	return heteroatoms + donors + acceptors
}

func main() {
	fmt.Printf("benzene_DBE=%.6f\n", DBE(6.0, 6.0, 0.0, 0.0))
	fmt.Printf("acetic_acid_DBE=%.6f\n", DBE(2.0, 4.0, 0.0, 0.0))
	fmt.Printf("polarity_score=%.6f\n", PolarityScore(2.0, 1.0, 2.0))
}
