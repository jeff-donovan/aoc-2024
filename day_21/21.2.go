package main

import (
	"bufio"
	"fmt"
	"os"
)

var NUMERICAL_KEYPAD = map[string]map[string]string{
	"A": {
		"^": "3",
		"<": "0",
	},
	"0": {
		"^": "2",
		">": "A",
	},
	"1": {
		"^": "4",
		">": "2",
	},
	"2": {
		"^": "5",
		"v": "0",
		"<": "1",
		">": "3",
	},
	"3": {
		"^": "6",
		"v": "A",
		"<": "2",
	},
	"4": {
		"^": "7",
		"v": "1",
		">": "5",
	},
	"5": {
		"^": "8",
		"v": "2",
		"<": "4",
		">": "6",
	},
	"6": {
		"^": "9",
		"v": "3",
		"<": "5",
	},
	"7": {
		"v": "4",
		">": "8",
	},
	"8": {
		"v": "5",
		"<": "7",
		">": "9",
	},
	"9": {
		"v": "6",
		"<": "8",
	},
}

var DIRECTIONAL_KEYPAD = map[string]map[string]string{
	"A": {
		"<": "^",
		"v": ">",
	},
	"^": {
		">": "A",
		"v": "v",
	},
	"<": {
		">": "v",
	},
	">": {
		"<": "v",
		"^": "A",
	},
	"v": {
		"<": "<",
		">": ">",
		"^": "^",
	},
}

func makeCodes(f *os.File) ([]string, error) {
	var codes []string
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		codes = append(codes, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return codes, nil
}

func main() {
	f, err := os.Open("day_21/day_21_test.txt")
	if err != nil {
		fmt.Println("Error opening file", err)
		return
	}

	defer f.Close()
	codes, err := makeCodes(f)
	if err != nil {
		fmt.Println("Error reading file:", err)
	}

	fmt.Println("codes: ", codes)
}
