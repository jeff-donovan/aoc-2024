'''
--- Part Two ---
The reindeer spends a few minutes reviewing your hiking trail map before realizing something, disappearing for a few minutes, and finally returning with yet another slightly-charred piece of paper.

The paper describes a second way to measure a trailhead called its rating. A trailhead's rating is the number of distinct hiking trails which begin at that trailhead. For example:

.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
The above map has a single trailhead; its rating is 3 because there are exactly three distinct hiking trails which begin at that position:

.....0.   .....0.   .....0.
..4321.   .....1.   .....1.
..5....   .....2.   .....2.
..6....   ..6543.   .....3.
..7....   ..7....   .....4.
..8....   ..8....   ..8765.
..9....   ..9....   ..9....
Here is a map containing a single trailhead with rating 13:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....
This map contains a single trailhead with rating 227 (because there are 121 distinct hiking trails that lead to the 9 on the right edge and 106 that lead to the 9 on the bottom edge):

012345
123456
234567
345678
4.6789
56789.
Here's the larger example from before:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
Considering its trailheads in reading order, they have ratings of 20, 24, 10, 4, 1, 4, 5, 8, and 5. The sum of all trailhead ratings in this larger example topographic map is 81.

You're not sure how, but the reindeer seems to have crafted some tiny flags out of toothpicks and bits of paper and is using them to mark trailheads on your topographic map. What is the sum of the ratings of all trailheads?
'''


def make_map(contents):
    return [[int(char) for char in line] for line in contents.split('\n') if line]

def sum_all_trailheads(map):
    total = 0
    trailheads = get_all_trailhead_coords(map)
    for trailhead in trailheads:
        trails = get_distinct_hiking_trails(map, trailhead)
        total += len(trails)
    return total

def get_all_trailhead_coords(map):
    trailheads = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads

def get_distinct_hiking_trails(map, trailhead):
    trails = set([(trailhead,)])
    for next_level in range(1, 10):
        new_trails = set([])
        for trail in trails:
            coords = trail[-1]
            next_coords = get_next_coords(map, next_level, coords)
            for next in next_coords:
                new_trails.add(trail + (next,))
        trails = new_trails
    return trails

def get_next_coords(map, next_level, current_coords):
    i, j = current_coords
    current_level = next_level - 1
    if map[i][j] != current_level:
        return []

    up = (i - 1, j)
    down = (i + 1, j)
    left = (i, j - 1)
    right = (i, j + 1)

    next_coords = []
    for coords in [up, down, left, right]:
        if is_in_map(map, coords[0], coords[1]) and next_level == map[coords[0]][coords[1]]:
            next_coords.append(coords)
    return next_coords

def is_in_map(map, i, j):
    return (0 <= i < len(map)) and (0 <= j < len(map[i]))

if __name__ == '__main__':
    with open('10/day_10_test.txt', 'r') as f:
        contents = f.read()

    map = make_map(contents)
    num = sum_all_trailheads(map)
    print(num)
