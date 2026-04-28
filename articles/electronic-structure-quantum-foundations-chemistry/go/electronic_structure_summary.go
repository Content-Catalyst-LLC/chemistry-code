package main

import (
	"fmt"
	"math"
)

const H = 6.62607015e-34
const C = 299792458.0
const EvToJ = 1.602176634e-19
const ElectronMass = 9.1093837139e-31

func HydrogenEnergyEV(n float64) float64 {
	return -13.6 / (n * n)
}

func PhotonWavelengthNM(deltaEnergyEV float64) float64 {
	deltaJ := deltaEnergyEV * EvToJ
	return (H * C / deltaJ) * 1.0e9
}

func ParticleInBoxEnergyEV(n float64, boxLengthNM float64) float64 {
	lengthM := boxLengthNM * 1.0e-9
	energyJ := (math.Pow(n, 2) * math.Pow(H, 2)) / (8.0 * ElectronMass * math.Pow(lengthM, 2))
	return energyJ / EvToJ
}

func main() {
	e1 := HydrogenEnergyEV(1.0)
	e2 := HydrogenEnergyEV(2.0)
	wavelength := PhotonWavelengthNM(math.Abs(e2 - e1))

	fmt.Printf("hydrogen_n1_energy_eV=%.6f\n", e1)
	fmt.Printf("hydrogen_n2_energy_eV=%.6f\n", e2)
	fmt.Printf("n2_to_n1_wavelength_nm=%.3f\n", wavelength)
	fmt.Printf("particle_box_n1_1nm_eV=%.6f\n", ParticleInBoxEnergyEV(1.0, 1.0))
}
