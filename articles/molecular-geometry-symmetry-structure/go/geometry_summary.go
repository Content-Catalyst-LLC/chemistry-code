package main

import (
	"fmt"
	"math"
)

func Distance(a [3]float64, b [3]float64) float64 {
	dx := a[0] - b[0]
	dy := a[1] - b[1]
	dz := a[2] - b[2]
	return math.Sqrt(dx*dx + dy*dy + dz*dz)
}

func Dot(a [3]float64, b [3]float64) float64 {
	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
}

func Subtract(a [3]float64, b [3]float64) [3]float64 {
	return [3]float64{a[0] - b[0], a[1] - b[1], a[2] - b[2]}
}

func AngleDegrees(a [3]float64, b [3]float64, c [3]float64) float64 {
	u := Subtract(a, b)
	v := Subtract(c, b)
	cosTheta := Dot(u, v) / (math.Sqrt(Dot(u, u)) * math.Sqrt(Dot(v, v)))
	if cosTheta > 1.0 {
		cosTheta = 1.0
	}
	if cosTheta < -1.0 {
		cosTheta = -1.0
	}
	return math.Acos(cosTheta) * 180.0 / math.Pi
}

func main() {
	oxygen := [3]float64{0.0, 0.0, 0.0}
	h1 := [3]float64{0.958, 0.0, 0.0}
	h2 := [3]float64{-0.239, 0.927, 0.0}

	fmt.Printf("OH distance angstrom=%.6f\n", Distance(oxygen, h1))
	fmt.Printf("HOH angle degrees=%.3f\n", AngleDegrees(h1, oxygen, h2))
}
