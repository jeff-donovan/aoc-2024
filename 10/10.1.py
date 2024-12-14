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
    with open('10/day_10_input.txt', 'r') as f:
        contents = f.read()

    map = make_map(contents)
    num = sum_all_trailheads(map)
    print(num)
