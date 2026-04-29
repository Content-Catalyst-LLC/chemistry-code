package main

import "fmt"

type WaterRecord struct {
	Site          string
	Medium        string
	Analyte       string
	Concentration float64
	Unit          string
	Benchmark     float64
	FlowLS        float64
}

func RatioToBenchmark(concentration float64, benchmark float64) float64 {
	return concentration / benchmark
}

func NutrientLoadKgDay(concentrationMgL float64, flowLS float64) float64 {
	return concentrationMgL * flowLS * 0.0864
}

func main() {
	records := []WaterRecord{
		{"River-A", "surface_water", "nitrate_as_N", 7.8, "mg/L", 10.0, 820.0},
		{"River-A", "surface_water", "phosphate_as_P", 0.18, "mg/L", 0.10, 820.0},
		{"Urban-D", "stormwater", "turbidity", 38.0, "NTU", 25.0, 210.0},
	}

	fmt.Println("Water chemistry screening example")
	for _, record := range records {
		ratio := RatioToBenchmark(record.Concentration, record.Benchmark)
		flag := "below_benchmark"
		if ratio > 1.0 {
			flag = "exceeds_benchmark"
		}

		fmt.Printf(
			"%s | %s | %s | %.3f %s | ratio %.3f | %s\n",
			record.Site,
			record.Medium,
			record.Analyte,
			record.Concentration,
			record.Unit,
			ratio,
			flag,
		)

		if record.Unit == "mg/L" && (record.Analyte == "nitrate_as_N" || record.Analyte == "phosphate_as_P") {
			fmt.Printf("  estimated load: %.3f kg/day\n", NutrientLoadKgDay(record.Concentration, record.FlowLS))
		}
	}
}
