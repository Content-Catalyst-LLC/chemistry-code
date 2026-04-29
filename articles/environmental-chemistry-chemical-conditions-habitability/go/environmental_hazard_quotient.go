package main

import (
	"fmt"
	"math"
)

type MonitoringRecord struct {
	Site          string
	Medium        string
	Analyte       string
	Concentration float64
	Benchmark     float64
	Unit          string
}

func HazardQuotient(concentration float64, benchmark float64) float64 {
	return concentration / benchmark
}

func FirstOrderConcentration(c0 float64, k float64, tDays float64) float64 {
	return c0 * math.Exp(-k*tDays)
}

func main() {
	records := []MonitoringRecord{
		{"River-A", "surface_water", "phosphate_as_P", 0.18, 0.10, "mg/L"},
		{"Wetland-B", "sediment", "lead", 42.0, 35.0, "mg/kg"},
		{"Urban-C", "air", "ozone", 0.071, 0.070, "ppm"},
	}

	fmt.Println("Environmental chemistry hazard quotient screening")
	for _, record := range records {
		hq := HazardQuotient(record.Concentration, record.Benchmark)
		flag := "below_benchmark"
		if hq > 1.0 {
			flag = "exceeds_benchmark"
		}
		fmt.Printf(
			"%s | %s | %s | %.4f %s | HQ %.3f | %s\n",
			record.Site,
			record.Medium,
			record.Analyte,
			record.Concentration,
			record.Unit,
			hq,
			flag,
		)
	}

	c0 := 100.0
	k := 0.08
	halfLife := math.Log(2.0) / k

	fmt.Printf("\nFirst-order half-life: %.2f days\n", halfLife)
	for day := 0.0; day <= 60.0; day += 10.0 {
		fmt.Printf("day %.0f: %.3f ug/L\n", day, FirstOrderConcentration(c0, k, day))
	}
}
