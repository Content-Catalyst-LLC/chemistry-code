package main

import (
	"fmt"
	"math"
)

func LennardJones(distance float64, epsilon float64, sigma float64) float64 {
	ratio := sigma / distance
	return 4.0 * epsilon * (math.Pow(ratio, 12) - math.Pow(ratio, 6))
}

func VelocityVerletPosition(position float64, velocity float64, acceleration float64, dt float64) float64 {
	return position + velocity*dt + 0.5*acceleration*dt*dt
}

func VelocityUpdate(velocity float64, acceleration float64, dt float64) float64 {
	return velocity + acceleration*dt
}

func DiffusionFromMSD(msd float64, time float64) float64 {
	return msd / (6.0 * time)
}

func main() {
	fmt.Printf("new_position=%.6f\n", VelocityVerletPosition(0.0, 0.05, 0.10, 0.5))
	fmt.Printf("new_velocity=%.6f\n", VelocityUpdate(0.05, 0.10, 0.5))
	fmt.Printf("lj_energy=%.6f\n", LennardJones(1.12, 1.0, 1.0))
	fmt.Printf("diffusion_estimate=%.6f\n", DiffusionFromMSD(4.21, 7.0))
}
