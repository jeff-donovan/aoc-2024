package main

import (
	"fmt"
	"math"
	"math/big"
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

	// initialA := new(big.Int).Exp(big.NewInt(8), big.NewInt(18), nil)
	initialA := new(big.Int)
	initialA.SetString("1047014855769602392064", 10)

	for len(constraints) > 0 {
		check := constraints[0]
		for !check(int(initialA.Int64())) {
			initialA.Add(initialA, big.NewInt(1))
		}
		fmt.Println(initialA.String())
		fmt.Println(initialA)
	}

	fmt.Println(initialA)
	fmt.Println("SOLUTION APPROACH 2 TOOK:", time.Since(start))
}
