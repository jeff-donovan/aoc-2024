package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"sync"
	"time"
)

type StartEnd struct {
	Start rune
	End   rune
}

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
	data  map[string]string
	mutex sync.RWMutex
}

func NewCache() *Cache {
	return &Cache{
		data: make(map[string]string),
	}
}

func (c *Cache) Set(key string, value string) {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.data[key] = value
}

func (c *Cache) Get(key string) (string, bool) {
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

func findShortestPathLengthForCode(cache *Cache, numericalPaths map[StartEnd][]string, code string, maxDepth int) int {
	depth0 := numericalToDirectional(numericalPaths, code)
	var pathLengths []int
	for _, seq := range depth0 {
		pathLengths = append(pathLengths, pathLength(cache, seq, maxDepth))
	}
	return slices.Min(pathLengths)
}

func pathLength(cache *Cache, seq string, maxDepth int) int {
	if maxDepth == 0 {
		return len(seq)
	}

	stringDepth := int(math.Ceil(float64(maxDepth) / float64(2)))
	parts := splitByA(seq)
	for i := 0; i < stringDepth; i++ {
		for pIndex, s := range parts {
			parts[pIndex] = nextString(cache, s)
		}
	}

	remainingDepth := maxDepth - stringDepth
	total := 0
	for _, p := range parts {
		for _, s := range splitByA(p) {
			total += pathLength(cache, s, remainingDepth)
		}
	}
	return total
}

func nextString(cache *Cache, seq string) string {
	value, found := cache.Get(seq)
	if found {
		return value
	}

	result := ""
	for _, part := range splitByA(seq) {
		result += nextString(cache, part)
	}
	cache.Set(seq, result)
	return result
}

func findShortestPathLengthRecursive(directionalPaths map[StartEnd][]string, groupByAPaths map[string][]string, seq string, currentDepth int, maxDepth int) int {
	if currentDepth == maxDepth {
		return len(seq)
	}

	total := 0
	for _, s := range groupByA(seq) {
		nextSequences := directionalToDirectional(directionalPaths, groupByAPaths, s)
		var pathLengths []int
		for _, ns := range nextSequences {
			pathLengths = append(pathLengths, findShortestPathLengthRecursive(directionalPaths, groupByAPaths, ns, currentDepth+1, maxDepth))
		}
		total += slices.Min(pathLengths)
	}
	return total
}

func numericalToDirectional(numericalPaths map[StartEnd][]string, code string) []string {
	sequences := []string{""}
	for i, end := range code {
		var start rune
		if i == 0 {
			start = 'A'
		} else {
			start = rune(code[i-1])
		}

		paths := numericalPaths[StartEnd{start, end}]
		var newSequences []string
		for _, path := range paths {
			for _, s := range sequences {
				newSequences = append(newSequences, s+path)
			}
		}
		sequences = newSequences
	}
	return tidyUp(sequences) // TODO: maybe we shouldn't tidy
}

func directionalToDirectional(directionalPaths map[StartEnd][]string, groupByAPaths map[string][]string, directionalSeq string) []string {
	value, found := groupByAPaths[directionalSeq]
	if found {
		return value
	}

	sequences := []string{""}
	for i, end := range directionalSeq {
		var start rune
		if i == 0 {
			start = 'A'
		} else {
			start = rune(directionalSeq[i-1])
		}

		paths := directionalPaths[StartEnd{start, end}]
		var newSequences []string
		for _, path := range paths {
			for _, seq := range sequences {
				newSequences = append(newSequences, seq+path)
			}
		}
		sequences = newSequences
	}
	return tidyUp(sequences) // TODO: maybe we shouldn't tidy
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
	for direction, nextStart := range keypad[start] {
		for _, path := range _findShortestPaths(keypad, nextStart, end, visited+string(start)) {
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

func calculateComplexity(code string, length int) int {
	codeNum, _ := strconv.Atoi(code[:len(code)-1])
	return codeNum * length
}

func calculateMinPathLength(paths []string) int {
	return len(slices.MinFunc(paths, func(a, b string) int {
		return len(a) - len(b)
	}))
}

func preComputeKeypadPaths(keypad Keypad) map[StartEnd][]string {
	paths := make(map[StartEnd][]string)
	for start := range keypad {
		for end := range keypad {
			paths[StartEnd{start, end}] = _findShortestPaths(keypad, start, end, "")
		}
	}
	return paths
}

func preComputeGroupByAPaths(numericalPaths map[StartEnd][]string, directionalPaths map[StartEnd][]string) map[string][]string {
	groupByASequences := make(map[string]struct{})
	for _, sequences := range numericalPaths {
		for _, seq := range sequences {
			groupByASequences[seq] = struct{}{}
		}
	}
	for _, sequences := range directionalPaths {
		for _, seq := range sequences {
			groupByASequences[seq] = struct{}{}
		}
	}

	groupByAPaths := make(map[string][]string)
	emptyMap := make(map[string][]string)
	for seq := range groupByASequences {
		groupByAPaths[seq] = directionalToDirectional(directionalPaths, emptyMap, seq)
	}
	return groupByAPaths
}

func preComputeGroupByAWinners(directionalPaths map[StartEnd][]string, groupByAPaths map[string][]string) *Cache {
	maxDepth := 1 // TODO: change to see if we get a diff shortest path length
	winners := NewCache()
	for aSeq, depth0 := range groupByAPaths {
		var shortestPathLengths []int
		for _, seq := range depth0 {
			shortestPathLengths = append(shortestPathLengths, findShortestPathLengthRecursive(directionalPaths, groupByAPaths, seq, 0, maxDepth))
		}
		for i, seq := range depth0 {
			if shortestPathLengths[i] == slices.Min(shortestPathLengths) {
				winners.Set(aSeq, seq)
			}
		}
	}
	return winners
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
	fmt.Println(codes)

	start := time.Now()

	numericalPaths := preComputeKeypadPaths(NUMERICAL_KEYPAD)
	directionalPaths := preComputeKeypadPaths(DIRECTIONAL_KEYPAD)
	groupByAPaths := preComputeGroupByAPaths(numericalPaths, directionalPaths)
	cache := preComputeGroupByAWinners(directionalPaths, groupByAPaths)

	depth := 2

	var complexities []int
	for _, code := range codes {
		complexities = append(complexities, calculateComplexity(code, findShortestPathLengthForCode(cache, numericalPaths, code, depth)))
	}

	total := 0
	for _, c := range complexities {
		total += c
	}
	fmt.Println(total)

	fmt.Println("took: ", time.Since(start))
}
