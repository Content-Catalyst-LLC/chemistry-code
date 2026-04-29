package main

import (
	"fmt"
	"math"
)

func MichaelisMenten(substrate float64, vmax float64, km float64) float64 {
	return vmax * substrate / (km + substrate)
}

func Occupancy(ligand float64, kd float64) float64 {
	return ligand / (kd + ligand)
}

func HillOccupancy(ligand float64, kd float64, n float64) float64 {
	return math.Pow(ligand, n) / (math.Pow(kd, n) + math.Pow(ligand, n))
}

func DeltaGStandard(k float64, temperatureK float64) float64 {
	const R = 8.314462618
	return -(R * temperatureK * math.Log(k)) / 1000.0
}

func main() {
	fmt.Printf("velocity=%.6f\n", MichaelisMenten(5.0, 120.0, 3.5))
	fmt.Printf("occupancy=%.6f\n", Occupancy(2.0, 2.0))
	fmt.Printf("hill_occupancy=%.6f\n", HillOccupancy(2.0, 2.0, 2.0))
	fmt.Printf("delta_g_kj_mol=%.6f\n", DeltaGStandard(1000.0, 298.15))
}
