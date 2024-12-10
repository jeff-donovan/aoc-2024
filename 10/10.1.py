'''
--- Day 10: Hoof It ---
You all arrive at a Lava Production Facility on a floating island in the sky. As the others begin to search the massive industrial complex, you feel a small nose boop your leg and look down to discover a reindeer wearing a hard hat.

The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly.

Perhaps you can help fill in the missing hiking trails?

The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest). For example:

0123
1234
8765
9876
Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).

You look up from the map and notice that the reindeer has helpfully begun to construct a small pile of pencils, markers, rulers, compasses, stickers, and other equipment you might need to update the map with hiking trails.

A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail. In the above example, the single trailhead in the top left corner has a score of 1 because it can reach a single 9 (the one in the bottom left).

This trailhead has a score of 2:

...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
(The positions marked . are impassable tiles to simplify these examples; they do not appear on your actual topographic map.)

This trailhead has a score of 4 because every 9 is reachable via a hiking trail except the one immediately to the left of the trailhead:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....
This topographic map contains two trailheads; the trailhead at the top has a score of 1, while the trailhead at the bottom has a score of 2:

10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
Here's a larger example:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
This larger example has 9 trailheads. Considering the trailheads in reading order, they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of all trailheads is 36.

The reindeer gleefully carries over a protractor and adds it to the pile. What is the sum of the scores of all trailheads on your topographic map?
'''


def make_map(contents):
    return [[int(char) for char in line] for line in contents.split('\n') if line]

def sum_all_trailheads(map):
    total = 0
    trailheads = get_all_trailhead_coords(map)
    for trailhead in trailheads:
        unique_peaks = get_peaks(map, trailhead)
        total += len(unique_peaks)
    return total

def get_all_trailhead_coords(map):
    trailheads = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 0:
                trailheads.append((i, j))
    return trailheads

def get_peaks(map, trailhead):
    trail_coords = set([trailhead])
    for next_level in range(1, 10):
        next_coords = []
        for coords in trail_coords:
            next_coords += get_next_coords(map, next_level, coords)
        trail_coords = set(next_coords)
    return trail_coords

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
