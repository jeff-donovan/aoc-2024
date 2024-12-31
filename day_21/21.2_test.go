package main

import (
	"fmt"
	"reflect"
	"testing"
)

func TestCartesianProduct(t *testing.T) {
	tests := []struct {
		name     string
		input    [][]string
		expected [][]string
	}{
		{
			name:     "Empty input",
			input:    [][]string{},
			expected: [][]string{{}},
		},
		{
			name:     "Single input",
			input:    [][]string{{"A", "B"}},
			expected: [][]string{{"A"}, {"B"}},
		},
		{
			name:     "Two inputs",
			input:    [][]string{{"A", "B"}, {"1", "2"}},
			expected: [][]string{{"A", "1"}, {"A", "2"}, {"B", "1"}, {"B", "2"}},
		},
		{
			name:     "Three inputs",
			input:    [][]string{{"A"}, {"1", "2"}, {"X", "Y"}},
			expected: [][]string{{"A", "1", "X"}, {"A", "1", "Y"}, {"A", "2", "X"}, {"A", "2", "Y"}},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := cartesianProduct(tt.input...)
			if !reflect.DeepEqual(result, tt.expected) {
				t.Errorf("Failed %s: got %v, want %v", tt.name, result, tt.expected)
			}
		})
	}
}

func TestNumericalToDirectional(t *testing.T) {
	cache := NewCache()
	fmt.Println(numericalToDirectional(cache, "980A"))
	fmt.Println(directionalToDirectional(cache, "^^^A<AvvvA>A"))
	fmt.Println(directionalToDirectional(cache, "<AAA>Av<<A>>^Av<AAA>^AvA^A"))
}
