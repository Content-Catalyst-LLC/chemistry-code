package main

import (
	"fmt"
	"math"
)

func Tanimoto(a float64, b float64, c float64) float64 {
	return c / (a + b - c)
}

func PIC50(ic50NM float64) float64 {
	ic50M := ic50NM * 1.0e-9
	return -math.Log10(ic50M)
}

func EuclideanDistance(x []float64, y []float64) float64 {
	sum := 0.0
	for i := range x {
		delta := x[i] - y[i]
		sum += delta * delta
	}
	return math.Sqrt(sum)
}

func main() {
	fmt.Printf("tanimoto=%.6f\n", Tanimoto(5.0, 4.0, 3.0))
	fmt.Printf("pIC50=%.6f\n", PIC50(50.0))
	fmt.Printf("distance=%.6f\n", EuclideanDistance([]float64{1.0, 2.0, 3.0}, []float64{1.5, 2.5, 4.0}))
}
