package main

import (
	"fmt"
	"math"
)

func SimulateNetwork(k1, k2, k3, k4, dt, totalTime float64) [5]float64 {
	a := 1.0
	b := 0.0
	c := 0.0
	d := 0.0
	e := 0.0

	for t := 0.0; t <= totalTime; t += dt {
		r1 := k1 * a
		r2 := k2 * b
		r3 := k3 * a
		r4 := k4 * b

		a = math.Max(a+(-r1-r3)*dt, 0.0)
		b = math.Max(b+(r1-r2-r4)*dt, 0.0)
		c = math.Max(c+r2*dt, 0.0)
		d = math.Max(d+r3*dt, 0.0)
		e = math.Max(e+r4*dt, 0.0)
	}

	return [5]float64{a, b, c, d, e}
}

func main() {
	result := SimulateNetwork(0.20, 0.08, 0.05, 0.03, 0.25, 50.0)

	fmt.Printf("A_final=%.6f\n", result[0])
	fmt.Printf("B_final=%.6f\n", result[1])
	fmt.Printf("C_final=%.6f\n", result[2])
	fmt.Printf("D_final=%.6f\n", result[3])
	fmt.Printf("E_final=%.6f\n", result[4])
}
