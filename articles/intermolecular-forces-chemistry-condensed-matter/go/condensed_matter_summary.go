package main

import (
	"fmt"
	"math"
)

func LennardJones(rAngstrom float64, epsilonKJMol float64, sigmaAngstrom float64) float64 {
	ratio := sigmaAngstrom / rAngstrom
	return 4.0 * epsilonKJMol * (math.Pow(ratio, 12) - math.Pow(ratio, 6))
}

func CoulombRelative(q1 float64, q2 float64, r float64) float64 {
	return q1 * q2 / r
}

func main() {
	epsilon := 0.997
	sigma := 3.40
	rMin := math.Pow(2.0, 1.0/6.0) * sigma
	uMin := LennardJones(rMin, epsilon, sigma)

	fmt.Printf("r_min_angstrom=%.6f\n", rMin)
	fmt.Printf("u_min_kj_mol=%.6f\n", uMin)
	fmt.Printf("relative_coulomb_attraction=%.6f\n", CoulombRelative(1.0, -1.0, 2.0))
}
