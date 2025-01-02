package main

import (
	"fmt"
	"math"
	"time"
)

type ConstraintFunc func(initialA int) bool

func main() {
	start := time.Now()

	constraints := []ConstraintFunc{
		func(initialA int) bool {
			return 2 == (((((initialA / 8) % 8) ^ 5) ^ ((initialA / 8) / int(math.Pow(2, float64(((initialA/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 4 == ((((((initialA / 8) / 8) % 8) ^ 5) ^ (((initialA / 8) / 8) / int(math.Pow(2, float64((((initialA/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 1 == (((((((initialA / 8) / 8) / 8) % 8) ^ 5) ^ ((((initialA / 8) / 8) / 8) / int(math.Pow(2, float64(((((initialA/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 5 == ((((((((initialA / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((initialA / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((initialA/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 7 == (((((((((initialA / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ ((((((initialA / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64(((((((initialA/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 5 == ((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((((initialA/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 4 == (((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ ((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64(((((((((initialA/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 5 == ((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 0 == (((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ ((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64(((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 3 == ((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 1 == (((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ ((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64(((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 6 == ((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 5 == (((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ ((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64(((((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 5 == ((((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 3 == (((((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ ((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64(((((((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
		func(initialA int) bool {
			return 0 == ((((((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) % 8) ^ 5) ^ (((((((((((((((((initialA / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / 8) / int(math.Pow(2, float64((((((((((((((((((initialA/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)/8)%8)^5)))) ^ 6) % 8)
		},
	}

	initialA := int(math.Pow(8, 17))

	for len(constraints) > 0 {
		check := constraints[0]
		constraints = constraints[1:]
		for !check(initialA) {
			initialA++
		}
		fmt.Println(initialA)
	}

	fmt.Println(initialA)
	fmt.Println("SOLUTION APPROACH 2 TOOK:", time.Since(start))
}
