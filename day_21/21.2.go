package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
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

func numericalToDirectional(cache *Cache, code string) []string {
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
			for _, s := range sequences {
				newSequences = append(newSequences, s+path)
			}
		}
		sequences = newSequences
	}
	return sequences
}

func directionalToDirectional(cache *Cache, seq string) []string {
	var value []string
	cacheKey := "directional_to_directional" + seq
	value, found := cache.Get(cacheKey)
	if found {
		return value
	}

	parts := splitByA(seq)
	if len(parts) == 1 {
		value = directionalToDirectionalWithWinner(cache, seq) // NOTE: there is a big assumption here that directionalToDirectionalWithWinner produces a single element slice
		cache.Set(cacheKey, value)
		return value
	}

	var sequences []string
	for _, prod := range cartesianProduct([][]string{directionalToDirectional(cache, parts[0]), directionalToDirectional(cache, parts[1])}...) {
		sequences = append(sequences, strings.Join(prod, ""))
	}
	cache.Set(cacheKey, sequences)
	return sequences
}

// Stole from Python's itertools.product - https://docs.python.org/3/library/itertools.html#itertools.product
func cartesianProduct(iterables ...[]string) [][]string {
	result := [][]string{{}}

	for _, pool := range iterables {
		var newResult [][]string
		for _, x := range result {
			for _, y := range pool {
				xCopy := make([]string, len(x))
				copy(xCopy, x)
				newResult = append(newResult, append(xCopy, y))
			}
		}
		result = newResult
	}

	return result
}

func directionalToDirectionalWithWinner(cache *Cache, seq string) []string {
	sequences := tidyUp(_directionalToDirectional(cache, seq))
	depth := 0
	for len(sequences) > 1 {
		if depth >= 3 {
			break
		}
		var minLengths []int
		for _, s := range sequences {
			minLengths = append(minLengths, calculateShortestPathLength(cache, s, depth))
		}

		var newSequences []string
		for i, s := range sequences {
			if minLengths[i] == slices.Min(minLengths) {
				newSequences = append(newSequences, s)
			}
		}

		sequences = newSequences
		depth++
	}
	return sequences
}

func calculateShortestPathLength(cache *Cache, seq string, depth int) int {
	var minPathLengths []int
	for _, aSeq := range groupByA(seq) {
		sequences := []string{aSeq}
		for i := 0; i < depth; i++ {
			// fmt.Printf("calculateShortestPathLength | %s | %d | %d\n", aSeq, i, len(sequences))
			var newSequences []string
			for _, s := range sequences {
				newSequences = append(newSequences, _directionalToDirectional(cache, s)...)
			}
			sequences = tidyUp(newSequences)
		}
		minPathLengths = append(minPathLengths, calculateMinPathLength(sequences))
	}

	sum := 0
	for _, length := range minPathLengths {
		sum += length
	}
	return sum
}

func _directionalToDirectional(cache *Cache, seq string) []string {
	sequences := []string{""}
	for i, end := range seq {
		var start rune
		if i == 0 {
			start = 'A'
		} else {
			start = rune(seq[i-1])
		}

		var newSequences []string
		for _, path := range findShortestPaths(cache, DIRECTIONAL_KEYPAD, start, end) {
			for _, s := range sequences {
				newSequences = append(newSequences, s+path)
			}
		}
		sequences = newSequences
	}
	return sequences
}

func splitByA(seq string) []string {
	var aIndices []int
	for i, char := range seq {
		if char == 'A' {
			aIndices = append(aIndices, i)
		}
	}

	numAIndices := len(aIndices)
	if numAIndices < 2 {
		return []string{seq}
	}

	splitIndex := aIndices[numAIndices/2-1]
	firstHalf := seq[:splitIndex+1]
	secondHalf := seq[splitIndex+1:]
	return []string{firstHalf, secondHalf}
}

func groupByA(seq string) []string {
	var aIndices []int
	for i, char := range seq {
		if char == 'A' {
			aIndices = append(aIndices, i)
		}
	}

	var sequences []string
	start := 0
	for _, aIndex := range aIndices {
		sequences = append(sequences, seq[start:aIndex+1])
		start = aIndex + 1
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

func calculateComplexity(code string, sequences []string) int {
	codeNum, _ := strconv.Atoi(code[:len(code)-1])
	return codeNum * calculateMinPathLength(sequences)
}

func calculateMinPathLength(paths []string) int {
	return len(slices.MinFunc(paths, func(a, b string) int {
		return len(a) - len(b)
	}))
}

func main() {
	f, err := os.Open("C:/code/aoc-2024/day_21/day_21_input.txt")
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

	depth := 10

	var complexities []int
	for _, code := range codes {
		sequences := numericalToDirectional(cache, code)
		for i := 0; i < depth; i++ {
			fmt.Printf("%s - depth %d\n", code, i)
			var newSequences []string
			for _, seq := range sequences {
				newSequences = append(newSequences, directionalToDirectional(cache, seq)...)
			}
			sequences = newSequences
		}
		complexities = append(complexities, calculateComplexity(code, sequences))
	}

	// fmt.Println(directionalToDirectional(cache, "<A^A>^^AvvvA"))

	total := 0
	for _, c := range complexities {
		total += c
	}
	fmt.Println(total)
}
