// Food Chemistry and the Molecular Basis of Nutrition
// Go food chemistry analytics example.
// Synthetic educational code only.

package main

import (
	"fmt"
	"math"
	"os"
)

type Food struct {
	Name                  string
	EnergyKcal            float64
	ProteinG              float64
	FiberG                float64
	PotassiumMg           float64
	ProcessingIntensity   float64
	RetentionFactor       float64
	VitaminCMg             float64
	BioavailabilityFactor  float64
	IronMg                float64
}

func clamp01(x float64) float64 {
	return math.Max(0.0, math.Min(1.0, x))
}

func nutrientDensity(food Food) float64 {
	beneficial := 0.40*clamp01(food.ProteinG/25.0) +
		0.35*clamp01(food.FiberG/12.0) +
		0.25*clamp01(food.PotassiumMg/800.0)

	energyFactor := math.Max(food.EnergyKcal/100.0, 0.5)
	return beneficial / energyFactor
}

func retainedVitaminC(food Food) float64 {
	return food.VitaminCMg * food.RetentionFactor
}

func bioavailableIron(food Food) float64 {
	return food.IronMg * food.RetentionFactor * food.BioavailabilityFactor
}

func main() {
	os.MkdirAll("../outputs/tables", 0755)

	foods := []Food{
		{"lentils_cooked", 230, 18, 15, 730, 0.25, 0.88, 3, 0.16, 6.6},
		{"orange_segments", 80, 1.5, 4, 240, 0.15, 0.82, 70, 0.08, 0.2},
		{"spinach_cooked", 45, 5, 4, 840, 0.35, 0.72, 18, 0.07, 6.4},
	}

	file, err := os.Create("../outputs/tables/go_food_chemistry_metrics.csv")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	fmt.Fprintln(file, "food,nutrient_density,retained_vitamin_c_mg,bioavailable_iron_mg")

	for _, food := range foods {
		fmt.Fprintf(
			file,
			"%s,%.6f,%.6f,%.6f\n",
			food.Name,
			nutrientDensity(food),
			retainedVitaminC(food),
			bioavailableIron(food),
		)
	}

	fmt.Println("Go food chemistry metrics complete.")
}
