package main

import "fmt"

func SOCStockMgHa(socPercent float64, bulkDensity float64, depthCm float64) float64 {
	return socPercent * bulkDensity * depthCm
}

func BaseSaturationPercent(baseCations float64, cec float64) float64 {
	return 100.0 * baseCations / cec
}

func NitrogenBalance(inputs []float64, outputs []float64) float64 {
	totalInputs := 0.0
	totalOutputs := 0.0

	for _, value := range inputs {
		totalInputs += value
	}
	for _, value := range outputs {
		totalOutputs += value
	}

	return totalInputs - totalOutputs
}

func main() {
	fmt.Println("Soil chemistry calculations")

	socStock := SOCStockMgHa(1.8, 1.32, 30.0)
	baseSaturation := BaseSaturationPercent(8.4, 12.0)

	fmt.Printf("Field-A SOC stock: %.2f Mg/ha\n", socStock)
	fmt.Printf("Field-A base saturation: %.1f%%\n", baseSaturation)

	fieldBNetN := NitrogenBalance(
		[]float64{165.0, 35.0, 20.0},
		[]float64{145.0, 28.0, 22.0},
	)

	fmt.Printf("Field-B net nitrogen balance: %.2f kg/ha\n", fieldBNetN)
}
