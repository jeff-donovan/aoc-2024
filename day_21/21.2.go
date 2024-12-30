package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"sync"
)

type Keypad map[rune]map[rune]rune

var NUMERICAL_KEYPAD = Keypad{
	'A': {
		'^': '3',
		'<': '0',
	},
	'0': {
		'^': '2',
		'>': 'A',
	},
	'1': {
		'^': '4',
		'>': '2',
	},
	'2': {
		'^': '5',
		'v': '0',
		'<': '1',
		'>': '3',
	},
	'3': {
		'^': '6',
		'v': 'A',
		'<': '2',
	},
	'4': {
		'^': '7',
		'v': '1',
		'>': '5',
	},
	'5': {
		'^': '8',
		'v': '2',
		'<': '4',
		'>': '6',
	},
	'6': {
		'^': '9',
		'v': '3',
		'<': '5',
	},
	'7': {
		'v': '4',
		'>': '8',
	},
	'8': {
		'v': '5',
		'<': '7',
		'>': '9',
	},
	'9': {
		'v': '6',
		'<': '8',
	},
}

var DIRECTIONAL_KEYPAD = Keypad{
	'A': {
		'<': '^',
		'v': '>',
	},
	'^': {
		'>': 'A',
		'v': 'v',
	},
	'<': {
		'>': 'v',
	},
	'>': {
		'<': 'v',
		'^': 'A',
	},
	'v': {
		'<': '<',
		'>': '>',
		'^': '^',
	},
}

type Cache struct {
	data  map[string][]string
	mutex sync.RWMutex
}

func NewCache() *Cache {
	return &Cache{
		data: make(map[string][]string),
	}
}

func (c *Cache) Set(key string, value []string) {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.data[key] = value
}

func (c *Cache) Get(key string) ([]string, bool) {
	c.mutex.RLock()
	defer c.mutex.RUnlock()
	val, exists := c.data[key]
	return val, exists
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

func numericalToDirection(cache *Cache, code string) []string {
	sequences := []string{""}
	for i, end := range code {
		var start rune
		if i == 0 {
			start = 'A'
		} else {
			start = rune(code[i-1])
		}

		var newSequences []string
		for _, path := range findShortestPaths(cache, NUMERICAL_KEYPAD, start, end) {
			for _, seq := range sequences {
				newSequences = append(newSequences, seq+path)
			}
		}
		sequences = newSequences
	}
	return sequences
}

func findShortestPaths(cache *Cache, keypad Keypad, start rune, end rune) []string {
	var value []string
	cacheKey := string(start) + string(end)
	value, found := cache.Get(cacheKey)
	if !found {
		value = _findShortestPaths(keypad, start, end, "")
		cache.Set(cacheKey, value)
	}
	return value
}

func _findShortestPaths(keypad Keypad, start rune, end rune, visited string) []string {
	for _, char := range visited {
		if char == start {
			return nil
		}
	}

	if start == end {
		return []string{"A"}
	}

	var paths []string
	for direction, next_start := range keypad[start] {
		for _, path := range _findShortestPaths(keypad, next_start, end, visited+string(start)) {
			paths = append(paths, string(direction)+path)
		}
	}

	if len(paths) == 0 {
		return paths
	}

	return tidyUp(paths)
}

func tidyUp(paths []string) []string {
	minLength := calculateMinPathLength(paths)
	var result []string
	for _, path := range paths {
		if len(path) == minLength {
			result = append(result, path)
		}
	}
	return result
}

func calculateMinPathLength(paths []string) int {
	return len(slices.MinFunc(paths, func(a, b string) int {
		return len(a) - len(b)
	}))
}

func main() {
	f, err := os.Open("C:/code/aoc-2024/day_21/day_21_test.txt")
	if err != nil {
		fmt.Println("Error opening file", err)
		return
	}

	defer f.Close()
	codes, err := makeCodes(f)
	if err != nil {
		fmt.Println("Error reading file:", err)
	}

	cache := NewCache()
	for _, code := range codes {
		fmt.Println(numericalToDirection(cache, code))
	}
}
