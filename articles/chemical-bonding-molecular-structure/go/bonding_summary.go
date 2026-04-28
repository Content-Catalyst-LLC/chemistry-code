package main

import (
	"fmt"
	"math"
)

func BondOrder(bondingElectrons float64, antibondingElectrons float64) float64 {
	return (bondingElectrons - antibondingElectrons) / 2.0
}

func ElectronegativityDifference(chiA float64, chiB float64) float64 {
	return math.Abs(chiA - chiB)
}

func Distance(a [3]float64, b [3]float64) float64 {
	dx := a[0] - b[0]
	dy := a[1] - b[1]
	dz := a[2] - b[2]
	return math.Sqrt(dx*dx + dy*dy + dz*dz)
}

func main() {
	ohDistance := Distance([3]float64{0.0, 0.0, 0.0}, [3]float64{0.958, 0.0, 0.0})
	ohDeltaChi := ElectronegativityDifference(3.44, 2.20)
	h2BondOrder := BondOrder(2.0, 0.0)

	fmt.Printf("oh_distance_angstrom=%.6f\n", ohDistance)
	fmt.Printf("oh_delta_chi=%.6f\n", ohDeltaChi)
	fmt.Printf("h2_bond_order=%.6f\n", h2BondOrder)
}
