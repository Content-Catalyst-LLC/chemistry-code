package main

import (
	"fmt"
	"math"
)

func DoseResponse(concentration float64, ec50 float64, hill float64, bottom float64, top float64) float64 {
	return bottom + (top-bottom)/(1.0+math.Pow(ec50/concentration, hill))
}

func Occupancy(ligand float64, kd float64) float64 {
	return ligand / (kd + ligand)
}

func TargetEngagement(signalControl float64, signalTreated float64, signalMax float64) float64 {
	return (signalControl - signalTreated) / (signalControl - signalMax)
}

func main() {
	fmt.Printf("response=%.6f\n", DoseResponse(1.0, 1.5, 1.2, 0.05, 1.0))
	fmt.Printf("occupancy=%.6f\n", Occupancy(2.0, 2.0))
	fmt.Printf("target_engagement=%.6f\n", TargetEngagement(100.0, 55.0, 20.0))
}
