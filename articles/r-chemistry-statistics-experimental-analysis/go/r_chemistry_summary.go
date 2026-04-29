package main

import (
	"fmt"
	"math"
)

func Mean(values []float64) float64 {
	sum := 0.0
	for _, value := range values {
		sum += value
	}
	return sum / float64(len(values))
}

func SampleSD(values []float64) float64 {
	xbar := Mean(values)
	ss := 0.0
	for _, value := range values {
		ss += math.Pow(value-xbar, 2)
	}
	return math.Sqrt(ss / float64(len(values)-1))
}

func StandardError(values []float64) float64 {
	return SampleSD(values) / math.Sqrt(float64(len(values)))
}

func RSDPercent(values []float64) float64 {
	return 100.0 * SampleSD(values) / Mean(values)
}

func UnknownConcentration(response float64, slope float64, intercept float64) float64 {
	return (response - intercept) / slope
}

func main() {
	values := []float64{1.02, 1.05, 0.99}

	fmt.Printf("mean=%.6f\n", Mean(values))
	fmt.Printf("sample_sd=%.6f\n", SampleSD(values))
	fmt.Printf("standard_error=%.6f\n", StandardError(values))
	fmt.Printf("rsd_percent=%.6f\n", RSDPercent(values))
	fmt.Printf("unknown_concentration=%.6f\n", UnknownConcentration(0.95, 0.30, 0.02))
}
